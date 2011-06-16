from django.conf import settings

BLOG_PAGINATE_BY = getattr(settings, 'BLOG_PAGINATE_BY', 5)
BLOG_MULTIPLE_SITES = getattr(settings, 'BLOG_MULTIPLE_SITES', False)