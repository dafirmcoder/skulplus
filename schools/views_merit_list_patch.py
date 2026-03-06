from collections import Counter
from django.http import JsonResponse
from .models import Student, MarkSheet, StudentMark, Subject, ClassRoom
from .utils.grading import get_level_and_points_for_score
from django.shortcuts import get_object_or_404

def merit_lists_data(request):
    if not hasattr(request.user, 'headteacher'):
        return JsonResponse({'success': False, 'error': 'Forbidden'}, status=403)

    school = get_user_school(request.user)
    class_id = request.GET.get('class_id')
    exam_id = request.GET.get('exam_id')
    stream_id = request.GET.get('stream_id')
    term = (request.GET.get('term') or '').strip()

    classroom = get_object_or_404(ClassRoom, id=class_id, school=school)
    students = Student.objects.filter(classroom=classroom, school=school)
    if stream_id:
        students = students.filter(stream_id=stream_id)
    subjects = Subject.objects.filter(subjectallocation__class_id=class_id, school=school).distinct()

    # Find all marksheets for this class/exam
    mark_sheets = MarkSheet.objects.filter(school_class=classroom, exam_id=exam_id, status='published')
    if term:
        mark_sheets = mark_sheets.filter(term=term)
    mark_sheets = mark_sheets.select_related('subject')

    # Map: (student_id, subject_id) -> (score, out_of)
    marks_map = {}
    for mark in StudentMark.objects.filter(marksheet__in=mark_sheets, score__isnull=False):
        marks_map[(mark.student_id, mark.marksheet.subject_id)] = (mark.score, mark.marksheet.out_of)

    merit_list = []
    overall_level_counter = Counter()

    for student in students:
        total_points = 0
        level_list = []
        for subject in subjects:
            key = (student.id, subject.id)
            if key not in marks_map:
                continue
            score, out_of = marks_map[key]
            level, points = get_level_and_points_for_score(
                student=student,
                subject=subject,
                score=score,
                out_of=out_of,
                term=term
            )
            if points:
                total_points += points
            if level:
                level_list.append(level)
                overall_level_counter[level] += 1
        average_level = Counter(level_list).most_common(1)[0][0] if level_list else "-"
        merit_list.append({
            "adm": student.admission_number,
            "name": student.user.get_full_name() if hasattr(student, 'user') else str(student),
            "stream": student.stream.name if student.stream else "",
            "total_points": total_points,
            "average_level": average_level
        })
    # Rank
    merit_list.sort(key=lambda x: x["total_points"], reverse=True)
    return JsonResponse({
        "success": True,
        "students": merit_list,
        "analysis": dict(overall_level_counter)
    })
