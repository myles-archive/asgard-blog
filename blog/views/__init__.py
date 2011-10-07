import datetime, time

from django.views.generic import ListView, DetailView

from blog.models import Post
from blog.settings import BLOG_PAGINATE_BY
from blog.views.category import BlogCategoryDetailView, BlogCategoryListView
from blog.views.archive import BlogPostYearArchiveView, BlogPostMonthArchiveView, BlogPostDayArchiveView, BlogPostUpdatedArchiveView, BlogPostArchiveView

__all__ = [
	'BlogPostListView',
	'BlogPostDeatilView',
	'BlogCategoryListView',
	'BlogCategoryDetailView',
	'BlogPostYearArchiveView',
	'BlogPostMonthArchiveView',
	'BlogPostDayArchiveView',
	'BlogPostUpdatedArchiveView',
	'BlogPostArchiveView',
]

class BlogPostListView(ListView):
	
	context_object_name = "post_list"
	template_name = "blog/index.html"
	paginate_by = BLOG_PAGINATE_BY
	
	def get_queryset(self):
		return Post.objects.published().select_related()

class BlogPostDeatilView(DetailView):
	
	context_object_name = 'post'
	template_name = "blog/detail.html"
	
	def get_object(self):
		year = self.kwargs['year']
		month = self.kwargs['month']
		day = self.kwargs['day']
		slug = self.kwargs['slug']
		
		try:
			date = datetime.date(*time.strptime(year+month+day, '%Y%b%d')[:3])
		except ValueError:
			raise Http404
		
		try:
			return Post.objects.get_post(slug, date)
		except Post.DoesNotExist:
			raise Http404