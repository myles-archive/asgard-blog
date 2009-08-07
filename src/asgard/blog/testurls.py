from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

from asgard.blog.sitemaps import BlogPostSitemap, BlogCategorySitemap, BlogTagSitemap
from asgard.blog.feeds import BlogPostFeed, BlogCategoryPostFeed, BlogTagPostFeed

admin.autodiscover()

feeds = {
	'blog': BlogPostFeed,
	'blog-category': BlogCategoryPostFeed,
	'blog-tag': BlogTagPostFeed,
}

sitemaps = {
	'blog': BlogPostSitemap,
	'blog-category': BlogCategorySitemap,
	'blog-tag': BlogTagSitemap,
}

urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),
	(r'^comments/', include('django.contrib.comments.urls')),
	
	(r'^blog/', include('asgard.blog.urls')),
	
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