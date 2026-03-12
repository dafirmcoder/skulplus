from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone

from schools.access import get_user_school, user_has_permission
from schools.models import ClassRoom, Subject, TermDate

def _teacher_scope_or_forbidden(request):
    school = get_user_school(request.user)
    if not school:
        return None
    if getattr(request.user, 'teacher', None) or user_has_permission(request.user, school, 'academics_teacher'):
        return school
    return None

@login_required
def teacher_dashboard(request):
    return render(request, 'academics/teacher_dashboard.html')


@login_required
def scheme_generator(request):
    school = _teacher_scope_or_forbidden(request)
    if not school:
        return HttpResponseForbidden('Only teachers can access this module.')
    classes = ClassRoom.objects.filter(school=school).order_by('order', 'name')
    subjects = Subject.objects.filter(school=school).order_by('name')
    term_dates = TermDate.objects.filter(school=school).order_by('-year', '-term').first()
    terms = [
        {'id': td.id, 'label': f"{td.term} {td.year}"} for td in TermDate.objects.filter(school=school).order_by('-year', '-term')
    ]
    context = {
        'school_name': school.name,
        'school_logo_url': getattr(school, 'logo', None).url if getattr(school, 'logo', None) else '',
        'curriculum_type': getattr(school, 'school_type', '') or '',
        'classes': classes,
        'subjects': subjects,
        'terms': terms or [{'id': 'term1', 'label': 'Term 1'}, {'id': 'term2', 'label': 'Term 2'}, {'id': 'term3', 'label': 'Term 3'}],
        'term_dates': {
            'opening_date': term_dates.start_date if term_dates else '',
            'midterm_date': '',
            'closing_date': term_dates.end_date if term_dates else '',
            'total_weeks': ((term_dates.end_date - term_dates.start_date).days // 7 + 1) if term_dates else '',
        } if term_dates else None,
    }
    return render(request, 'academics/scheme_generator.html', context)


@login_required
def lessonplan_generator(request):
    school = _teacher_scope_or_forbidden(request)
    if not school:
        return HttpResponseForbidden('Only teachers can access this module.')
    classes = ClassRoom.objects.filter(school=school).order_by('order', 'name')
    subjects = Subject.objects.filter(school=school).order_by('name')
    context = {
        'school_name': school.name,
        'school_logo_url': getattr(school, 'logo', None).url if getattr(school, 'logo', None) else '',
        'curriculum_type': getattr(school, 'school_type', '') or '',
        'classes': classes,
        'subjects': subjects,
    }
    return render(request, 'academics/lessonplan_generator.html', context)


@login_required
def syllabus_coverage(request):
    school = _teacher_scope_or_forbidden(request)
    if not school:
        return HttpResponseForbidden('Only teachers can access this module.')
    context = {
        'school_name': school.name,
        'school_logo_url': getattr(school, 'logo', None).url if getattr(school, 'logo', None) else '',
        'curriculum_type': getattr(school, 'school_type', '') or '',
        'coverage_summary': {'subjects': 0, 'completed': 0, 'total': 0, 'percent': 0},
        'coverage_by_subject': [],
        'coverage_rows': [],
        'heatmap': [],
        'chart_data': {},
    }
    return render(request, 'academics/syllabus_coverage.html', context)


@login_required
def resources_dashboard(request):
    school = _teacher_scope_or_forbidden(request)
    if not school:
        return HttpResponseForbidden('Only teachers can access this module.')
    return render(request, 'academics/resources.html', {
        'school_name': school.name,
        'school_logo_url': getattr(school, 'logo', None).url if getattr(school, 'logo', None) else '',
        'curriculum_type': getattr(school, 'school_type', '') or '',
    })


@login_required
def reports_dashboard(request):
    school = _teacher_scope_or_forbidden(request)
    if not school:
        return HttpResponseForbidden('Only teachers can access this module.')
    return render(request, 'academics/reports.html', {
        'school_name': school.name,
        'school_logo_url': getattr(school, 'logo', None).url if getattr(school, 'logo', None) else '',
        'curriculum_type': getattr(school, 'school_type', '') or '',
    })
