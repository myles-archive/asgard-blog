import time
import datetime

from django.views.generic import TemplateView, ListView

from blog.models import Post
from blog.settings import BLOG_PAGINATE_BY

class BlogPostArchiveView(TemplateView):
	
	template_name = "blog/archive/archive.html"
	
	def get_context_data(self, **kwargs):
		posts = Post.objects.published()
		years = posts.dates('published', 'year')
		context = super(BlogPostArchiveView, self).get_context_data(**kwargs)
		context['archive'] = {}
		for year in years:
			context['archive'][year] = Post.objects.archvie_year(year).dates('published', 'month')
		return context

class BlogPostYearArchiveView(ListView):
	
	context_object_name = "post_list"
	template_name = "blog/archive/year.html"
	paginate_by = BLOG_PAGINATE_BY
	
	def get_context_data(self, **kwargs):
		context = super(BlogPostYearArchiveView, self).get_context_data(**kwargs)
		context['this_year'] = self.this_year
		context['next_year'] = self.this_year + datetime.timedelta(days=+366)
		context['prev_year'] = self.this_year + datetime.timedelta(days=-365)
		return context
	
	def get_queryset(self):
		self.this_year = datetime.date(int(self.kwargs['year']), 1, 1)
		return Post.objects.archvie_year(self.this_year).select_related()

class BlogPostMonthArchiveView(ListView):
	
	context_object_name = "post_list"
	template_name = "blog/archive/month.html"
	paginate_by = BLOG_PAGINATE_BY
	
	def get_context_data(self, **kwargs):
		first_day = self.this_month.replace(day=1)
		if first_day.month == 12:
			last_day = first_day.replace(year=first_day.year + 1, month=1)
		else:
			last_day = first_day.replace(month=first_day.month + 1)
		
		context = super(BlogPostMonthArchiveView, self).get_context_data(**kwargs)
		context['this_month'] = self.this_month
		context['next_month'] = last_day + datetime.timedelta(days=1)
		context['prev_month'] = first_day - datetime.timedelta(days=-1)
		return context
	
	def get_queryset(self):
		try:
			self.this_month = datetime.date(*time.strptime(self.kwargs['year']+self.kwargs['month'], '%Y%b')[:3])
		except ValueError:
			raise Http404
		
		return Post.objects.archive_month(self.this_month).select_related()

class BlogPostDayArchiveView(ListView):
	context_object_name = "post_list"
	template_name = "blog/archive/day.html"
	paginate_by = BLOG_PAGINATE_BY
	
	def get_context_data(self, **kwargs):
		context = super(BlogPostDayArchiveView, self).get_context_data(**kwargs)
		context['next_day'] = self.this_day + datetime.timedelta(days=+1)
		context['prev_day'] = self.this_day - datetime.timedelta(days=-1)
		context['this_day'] = self.this_day
		return context
	
	def get_queryset(self):
		try:
			self.this_day = datetime.date(*time.strptime(self.kwargs['year']+self.kwargs['month']+self.kwargs['day'], '%Y%b%d')[:3])
		except ValueError:
			raise Http404
		
		return Post.objects.archive_day(self.this_day).select_related()

class BlogPostUpdatedArchiveView(ListView):
	context_object_name = "post_list"
	template_name = "blog/archive/updated.html"
	paginate_by = BLOG_PAGINATE_BY
	
	def get_queryset(self):
		return Post.objects.updated()