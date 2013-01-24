DEBUG = True
DEBUG_TEMPLATE = True
SITE_ID = 1
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': '/tmp/asgard-blog-devel.db'
	}
}
INSTALLED_APPS = [
	'django.contrib.auth',
	'django.contrib.comments',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.admin',
	'django.contrib.sites',
	'django.contrib.sitemaps',
	
	'south',
	'django_markup',
	'taggit',
	
	'blog',
]
ROOT_URLCONF = 'blog.testurls'
SECRET_KEY = 'kz!=swngn%ifjrcru3rzovmhvbc@jlu3y5y#i=7%+--az%=+*%'
# BLOG_MULTIPLE_SITES = True