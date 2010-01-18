from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('blog.views',
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
		view = 'detail',
		name = 'blog_post_detail',
	),
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 
		view = 'archive_day',
		name = 'blog_archive_day',
	),
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
		view = 'archive_month',
		name = 'blog_archive_month',
	),
	url(r'^(?P<year>\d{4})/$',
		view = 'archive_year',
		name = 'blog_archive_year',
	),
	url(r'^tag/(?P<tag>(.*))/page/(?P<page>\d+)/$',
		view = 'tag_detail',
		name = 'blog_tag_detail_paginated',
	),
	url(r'^tag/(?P<tag>(.*))/$',
		view = 'tag_detail',
		name = 'blog_tags_detail',
	),
	url(r'^tag/$',
		view = 'tag_list',
		name = 'blog_tags_list'
	),
	url(r'^category/(?P<slug>[-\w]+)/page/(?P<page>\d+)/$',
		view = 'category_detail',
		name = 'blog_categories_detail_paginated',
	),
	url(r'^category/(?P<slug>[-\w]+)/$',
		view = 'category_detail',
		name = 'blog_categories_detail',
	),
	url (r'^category/$',
		view = 'category_list',
		name = 'blog_categories_list',
	),
	url(r'^search/$',
		view = 'search',
		name = 'blog_search',
	),
	url(r'^archive/$',
		view = 'archive',
		name = 'blog_archive'
	),
	url(r'^page/(?P<page>\d+)/$',
		view = 'index',
		name = 'blog_index_paginated',
	),
	url(r'^$',
		view = 'index',
		name = 'blog_index',
	),
)