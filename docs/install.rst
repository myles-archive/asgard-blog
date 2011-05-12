Installation instructions.
===========


Installing dependencies.
===========

# aptitude install python-setuptools

#easy_install django_taggit
#easy_install django_markup
#easy_install BeautifulSoup

Setting up blog on the system.
===========

$git clone <blog url (https://github.com/asgardproject/asgard-blog.git)>

* Change into source dir

$python setup.py build

#python setup.py install


Adding blog to a django project.
===========

* In settings.py, append the following to INSTALLED_APPS variable:

	'django.contrib.sitemaps',
	'django_markup',
	'django.contrib.comments',
	'taggit',
	'blog',
	
* In urls.py add the following:

#asgard-blog
from blog.sitemaps import BlogPostSitemap, BlogCategorySitemap, BlogTagSitemap, BlogAuthorSitemap
from blog.feeds import BlogPostFeed, BlogCategoryPostFeed, BlogTagPostFeed, BlogAuthorPostFeed

feeds = {
	'blog': BlogPostFeed,
	'blog-category': BlogCategoryPostFeed,
	'blog-tag': BlogTagPostFeed,
	'blog-author': BlogAuthorPostFeed
	}
	
sitemaps = {
	'blog': BlogPostSitemap,
	'blog-category': BlogCategorySitemap,
	'blog-tag': BlogTagSitemap,
	'blog-author': BlogAuthorSitemap
}

* Also in the same file, append this to your urlpatterns tuple:

(r'^blog/', include('blog.urls')),
(r'^comments/', include('django.contrib.comments.urls')),
url(r'^feeds/(?P<url>.*)/$','django.contrib.syndication.views.feed',{ 'feed_dict': feeds },	name = 'feeds'),
url(r'^sitemap.xml$','django.contrib.sitemaps.views.sitemap',{ 'sitemaps': sitemaps },name = 'sitemap'),

* At this point the blog should be up and running at <domain>/<project>/blog/ url or whatever you've specified in urls.py. Add blog posts from administrative interface.

* A word of warning, check that your timezone is set to correctly or the blog won't publish your that are set in the future even though they are set to have published status.

* Last step -- specify blog styling by copying base.html blog template from /usr/local/lib/python2.6/dist-packages/asgard_blog-0.3.0-py2.6.egg/blog/templates/ into your templates/ folder.


Debugging
===========

* Listing pots from django shell:

>>> from blog.models import Post
>>> Post.objects.all()
>>> Post.objects.public()
>>> Post.objects.published()