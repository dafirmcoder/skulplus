from .models import SiteConfig


def site_logo(request):
    """Add SITE_LOGO_URL and SITE_FAVICON_URL to template context when available.

    The context processor returns the most recently created SiteConfig if present.
    """
    try:
        cfg = SiteConfig.objects.order_by('-updated_at').first()
        if cfg:
            logo_url = cfg.logo.url if cfg.logo else None
            favicon_url = cfg.favicon.url if cfg.favicon else None
            return {'SITE_LOGO_URL': logo_url, 'SITE_FAVICON_URL': favicon_url}
    except Exception:
        pass
    return {'SITE_LOGO_URL': None, 'SITE_FAVICON_URL': None}
