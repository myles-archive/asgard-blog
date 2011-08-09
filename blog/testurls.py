from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

from blog.sitemaps import BlogPostSitemap, BlogCategorySitemap, BlogTagSitemap, BlogAuthorSitemap

admin.autodiscover()

sitemaps = {
	'blog': BlogPostSitemap,
	'blog-category': BlogCategorySitemap,
	'blog-tag': BlogTagSitemap,
	'blog-author': BlogAuthorSitemap
}

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^comments/', include('django.contrib.comments.urls')),
	
	url(r'^blog/', include('blog.urls')),
	
	url(r'^sitemap.xml$',
		'django.contrib.sitemaps.views.sitemap',
		{ 'sitemaps': sitemaps },
		name = 'sitemap'
	),
)
