from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

from blog.sitemaps import BlogPostSitemap, BlogCategorySitemap, BlogTagSitemap, BlogAuthorSitemap
from blog.feeds import BlogPostFeed, BlogCategoryPostFeed, BlogTagPostFeed, BlogAuthorPostFeed

admin.autodiscover()

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

urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),
	(r'^comments/', include('django.contrib.comments.urls')),
	
	(r'^blog/', include('blog.urls')),
	
	url(r'^feeds/(?P<url>.*)/$',
		'django.contrib.syndication.views.feed',
		{ 'feed_dict': feeds },
		name = 'feeds'
	),
	
	url(r'^sitemap.xml$',
		'django.contrib.sitemaps.views.sitemap',
		{ 'sitemaps': sitemaps },
		name = 'sitemap'
	),
)