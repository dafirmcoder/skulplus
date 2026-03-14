from .models import SiteConfig
from .access import get_user_role, get_user_school, user_has_permission, has_full_headteacher_access, user_has_user_management


def site_logo(request):
    """Add SITE_LOGO_URL and SITE_FAVICON_URL to template context when available.

    The context processor returns the most recently created SiteConfig if present.
    """
    try:
        cfg = SiteConfig.objects.order_by('-updated_at').first()
        if cfg:
            logo_url = cfg.logo.url if cfg.logo else None
            favicon_url = cfg.favicon.url if cfg.favicon else None
            logo_version = int(cfg.updated_at.timestamp()) if cfg.updated_at else None
            return {
                'SITE_LOGO_URL': logo_url,
                'SITE_FAVICON_URL': favicon_url,
                'SITE_ASSET_VERSION': logo_version,
            }
    except Exception:
        pass
    return {'SITE_LOGO_URL': None, 'SITE_FAVICON_URL': None, 'SITE_ASSET_VERSION': None}


def user_access_flags(request):
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return {}

    school = get_user_school(user)
    role = get_user_role(user, school)
    try:
        from .models import Student
        is_parent = Student.objects.filter(parent_user=user).exists()
        parent_student_count = Student.objects.filter(parent_user=user).count() if is_parent else 0
    except Exception:
        is_parent = False
        parent_student_count = 0
    teacher_competencies = False
    if hasattr(user, 'teacher') and school:
        try:
            from .models import TeacherAssignment, StreamClassTeacher, ClassRoom
            level_names = ('Pre School', 'Kindergarten')
            assigned_class_ids = set(
                TeacherAssignment.objects.filter(
                    teacher=user.teacher,
                    classroom__school=school,
                ).values_list('classroom_id', flat=True)
            )
            assigned_class_ids.update(
                StreamClassTeacher.objects.filter(
                    teacher=user.teacher,
                    classroom__school=school,
                ).values_list('classroom_id', flat=True)
            )
            assigned_class_ids.update(
                ClassRoom.objects.filter(
                    school=school,
                    class_teacher=user.teacher,
                ).values_list('id', flat=True)
            )
            if assigned_class_ids:
                teacher_competencies = ClassRoom.objects.filter(
                    id__in=assigned_class_ids,
                    level__name__in=level_names,
                ).exists()
        except Exception:
            teacher_competencies = False

    return {
        'ACCESS_ROLE': role or '',
        'ACCESS_CAN_FULL_DASHBOARD': has_full_headteacher_access(user, school),
        'ACCESS_CAN_USER_MGMT': user_has_user_management(user, school),
        'ACCESS_CAN_STUDENTS': user_has_permission(user, school, 'students'),
        'ACCESS_CAN_TEACHERS': user_has_permission(user, school, 'teachers'),
        'ACCESS_CAN_ACADEMICS': user_has_permission(user, school, 'academics'),
        'ACCESS_CAN_FINANCE': user_has_permission(user, school, 'finance'),
        'IS_PARENT_USER': is_parent,
        'PARENT_STUDENT_COUNT': parent_student_count,
        'ACCESS_CAN_COMPETENCIES': teacher_competencies,
    }
