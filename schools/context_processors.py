from .models import SiteConfig


def site_logo(request):
    """Add SITE_LOGO_URL and SITE_FAVICON_URL to template context when available.

    The context processor returns the most recently created SiteConfig if present.
    """
    try:
        cfg = SiteConfig.objects.order_by('-updated_at').first()
        if cfg and cfg.logo:
            return {'SITE_LOGO_URL': cfg.logo.url, 'SITE_FAVICON_URL': cfg.favicon.url if cfg.favicon else None}
    except Exception:
        pass
    return {'SITE_LOGO_URL': None, 'SITE_FAVICON_URL': None}
