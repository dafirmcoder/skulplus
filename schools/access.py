from __future__ import annotations

from typing import Iterable, Optional

from .models import School, SchoolUserAccess


ROLE_DEAN = SchoolUserAccess.ROLE_DEAN
ROLE_SECRETARY = SchoolUserAccess.ROLE_SECRETARY
ROLE_ACCOUNTS = SchoolUserAccess.ROLE_ACCOUNTS
ROLE_DEPUTY = SchoolUserAccess.ROLE_DEPUTY


def get_user_school(user) -> Optional[School]:
    if not getattr(user, 'is_authenticated', False):
        return None
    if hasattr(user, 'headteacher'):
        return user.headteacher.school
    if hasattr(user, 'teacher'):
        return user.teacher.school
    if getattr(user, 'is_superuser', False):
        return School.objects.first()
    access = SchoolUserAccess.objects.select_related('school').filter(user=user, is_active=True).first()
    return access.school if access else None


def get_user_role(user, school: Optional[School] = None) -> Optional[str]:
    if not getattr(user, 'is_authenticated', False):
        return None
    if getattr(user, 'is_superuser', False):
        return 'SUPERUSER'
    if hasattr(user, 'headteacher'):
        return 'HEADTEACHER'
    if school is None:
        school = get_user_school(user)
    if not school:
        return None
    access = SchoolUserAccess.objects.filter(user=user, school=school, is_active=True).first()
    if access:
        return access.role
    if hasattr(user, 'teacher'):
        return 'TEACHER'
    return None


def has_full_headteacher_access(user, school: Optional[School] = None) -> bool:
    role = get_user_role(user, school)
    return role in ('SUPERUSER', 'HEADTEACHER', ROLE_DEPUTY)


def user_has_permission(user, school: Optional[School], permission: str) -> bool:
    role = get_user_role(user, school)
    if role in ('SUPERUSER', 'HEADTEACHER', ROLE_DEPUTY):
        return True
    if role == ROLE_DEAN:
        return permission in {'academics', 'students', 'teachers'}
    if role == ROLE_SECRETARY:
        return permission in {'students'}
    if role == ROLE_ACCOUNTS:
        return permission in {'finance'}
    if role == 'TEACHER':
        if permission in {'academics_teacher'}:
            return True
        if permission == 'students' and hasattr(user, 'teacher') and user.teacher.is_class_teacher:
            return True
        if permission == 'academics' and hasattr(user, 'teacher') and user.teacher.is_class_teacher:
            return True
        return False
    return False


def user_has_user_management(user, school: Optional[School] = None) -> bool:
    role = get_user_role(user, school)
    return role in ('SUPERUSER', 'HEADTEACHER', ROLE_DEPUTY, ROLE_DEAN)


def user_has_any_permission(user, school: Optional[School], permissions: Iterable[str]) -> bool:
    return any(user_has_permission(user, school, p) for p in permissions)
