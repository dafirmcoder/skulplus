from .models import SiteConfig
from .access import get_user_role, get_user_school, user_has_permission, has_full_headteacher_access


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
    return {
        'ACCESS_ROLE': role or '',
        'ACCESS_CAN_FULL_DASHBOARD': has_full_headteacher_access(user, school),
        'ACCESS_CAN_STUDENTS': user_has_permission(user, school, 'students'),
        'ACCESS_CAN_TEACHERS': user_has_permission(user, school, 'teachers'),
        'ACCESS_CAN_ACADEMICS': user_has_permission(user, school, 'academics'),
        'ACCESS_CAN_FINANCE': user_has_permission(user, school, 'finance'),
    }
