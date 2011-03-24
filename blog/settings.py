from django.conf import settings

BLOG_MUTIPLE_SITE = getattr(settings, 'BLOG_MUTIPLE_SITE', False)