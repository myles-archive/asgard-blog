DEBUG = True
DEBUG_TEMPLATE = True
SITE_ID = 1
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/asgard-blog-devel.db'
INSTALLED_APPS = [
	'asgard.blog',
]
ROOT_URLCONF = 'asgard.blog.urls'