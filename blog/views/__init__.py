import datetime, time

from django.http import Http404

from django.core.paginator import (
	Paginator,
	InvalidPage,
	EmptyPage
)

from django.views.generic.base import (
	View,
	ContextMixin,
	TemplateResponseMixin
)

from blog.models import Post
from blog.settings import BLOG_PAGINATE_BY

from blog.views.category import (
	BlogCategoryDetailView, BlogCategoryListView
)
from blog.views.archive import (
	BlogPostYearArchiveView, BlogPostMonthArchiveView,
	BlogPostDayArchiveView, BlogPostUpdatedArchiveView,
	BlogPostArchiveView, BlogPostWeekDayArchiveView,
	BlogPostWeekArchiveView
)
from blog.views.author import (
	BlogPostAuthorListView, BlogPostAuthorDetailView
)
from blog.views.search import BlogPostSearchFormListView
from blog.views.tag import (
	BlogTagListView, BlogTagDetailView
)

from blog.views.old import (
	index, archive, archive_year, archive_month, archive_day, detail,
	category_list, category_detail, author_list, author_detail,
	tag_list, tag_detail, search, updated
)

__all__ = [
	'BlogPostListView', 'BlogPostDeatilView',
	'BlogCategoryListView', 'BlogCategoryDetailView',
	'BlogPostYearArchiveView', 'BlogPostMonthArchiveView',
	'BlogPostWeekArchiveView', 'BlogPostWeekDayArchiveView',
	'BlogPostDayArchiveView', 'BlogPostUpdatedArchiveView',
	'BlogPostArchiveView', 'BlogPostSearchFormListView',
	'BlogPostAuthorListView', 'BlogPostAuthorDetailView',
	'BlogPostSearchFormListView', 'BlogTagListView',
	'BlogTagDetailView',

	'index', 'archive', 'archive_year', 'archive_month', 'archive_day',
	'detail', 'category_list', 'category_detail', 'author_list',
	'author_detail', 'tag_list', 'tag_detail', 'search', 'updated'
]

class BlogPostListView(TemplateResponseMixin, ContextMixin, View):

	template_name = 'blog/index.html'
	
	def get(self, request, page=1, count=BLOG_PAGINATE_BY, *args, **kwargs):
		post_list = Post.objects.published().select_related()
		
		if not posts_list:
		    raise Http404
		
		paginator = Paginator(post_list, int(request.GET.get('count', count)))
		
		try:
			posts = paginator.page(int(request.GET.get('page', page)))
		except (EmptyPage, InvalidPage):
			posts = paginator.page(paginator.num_pages)
		
		context = self.get_context_data(post_list=posts)
		
		return self.render_to_response(context)

class BlogPostDeatilView(TemplateResponseMixin, ContextMixin, View):
	
	template_name = 'blog/detail.html'

	def get(self, request, year, month, day, slug, *args, **kwargs):
		try:
			date = datetime.date(*time.strptime(year+month+day, '%Y%b%d')[:3])
		except ValueError:
			raise Http404
		
		try:
			post = Post.objects.get_post(slug, date)
		except Post.DoesNotExist:
			raise Http404

		context = self.get_context_data(post=post)

		return self.render_to_response(context)

class BlogPostSimpleDetailView(TemplateResponseMixin, ContextMixin, View):

	tempalte_name = 'blog/detail.html'

	def get(self, request, pk, slug, *args, **kwargs):

		try:
			post = Post.objects.get(pk=pk, slug__iexact=slug)
		except Post.DoesNotExist:
			raise Http404

		context = self.get_context_data(post=post)

		return self.render_to_response(context)
