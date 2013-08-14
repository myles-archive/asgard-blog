import time
import datetime

from django.http import Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.base import View, ContextMixin, TemplateResponseMixin

from blog.models import Post
from blog.settings import BLOG_PAGINATE_BY

__all__ = [
	'BlogPostYearArchiveView',
	'BlogPostMonthArchiveView',
	'BlogPostWeekArchiveView',
	'BlogPostWeekDayArchiveView',
	'BlogPostDayArchiveView',
	'BlogPostUpdatedArchiveView',
	'BlogPostArchiveView'
]

class BlogPostArchiveView(TemplateResponseMixin, ContextMixin, View):

	template_name = "blog/archive/archive.html"

	def get_context_data(self, **kwargs):
		context = super(BlogPostArchiveView, self).get_context_data(**kwargs)

		context['archive'] = {}

		posts = Post.objects.published()
		years = posts.dates('published', 'year')
		
		for year in years:
			context['archive'][year] = Post.objects.archvie_year(year).dates('published', 'month')
		
		return context

	def get(self, request, **kwargs):
		context = self.get_context_data()

		return self.render_to_response(context)

class BlogPostYearArchiveView(TemplateResponseMixin, ContextMixin, View):

	template_name = "blog/archive/year.html"

	def get(self, request, year, *args, **kwargs):
		this_year = datetime.date(int(year), 1, 1)

		posts = Post.objects.archvie_year(this_year).select_related()

		next_year = this_year + datetime.timedelta(days=+366)
		prev_year = this_year + datetime.timedelta(days=-365)

		context = self.get_context_data()

		context = {
			'post_list': posts,
			'this_year': this_year,
			'next_year': next_year,
			'prev_year': prev_year,
		}

		return self.render_to_response(context)

class BlogPostMonthArchiveView(TemplateResponseMixin, ContextMixin, View):

	template_name = "blog/archive/month.html"

	def get(self, request, year, month, *args, **kwargs):
		try:
			date = datetime.date(*time.strptime(year+month, '%Y%b')[:3])
		except ValueError:
			raise Http404

		posts = Post.objects.archive_month(date).select_related()

		first_day = date.replace(day=1)
		if first_day.month == 12:
			last_day = first_day.replace(year=first_day.year + 1, month=1)
		else:
			last_day = first_day.replace(month=first_day.month + 1)

		next_month = last_day + datetime.timedelta(days=1)
		prev_month = first_day - datetime.timedelta(days=-1)

		context = self.get_context_data()

		context = {
			'post_list': posts,
			'this_month': date,
			'next_month': next_month,
			'prev_month': prev_month,
		}

		return self.render_to_response(context)

class BlogPostWeekDayArchiveView(TemplateResponseMixin, ContextMixin, View):
	
	template_name = "blog/archive/weekday.html"
	
	def get(self, request, year, week, weekday, *args, **kwargs):
		try:
			this_day = datetime.date(*time.strptime("%s-%s-%s" % (year, week, weekday), "%Y-%U-%a")[:3])
		except ValueError:
			raise Http404
		
		next_day = this_day + datetime.timedelta(days=+1)
		prev_day = this_day - datetime.timedelta(days=-1)
		
		posts = Post.objects.archive_day(this_day).select_related()
		
		context = self.get_context_data()
		
		context = {
			'post_list': posts,
			'this_day': this_day,
			'next_day': next_day,
			'prev_day': prev_day,
		}
		
		return self.render_to_response(context)

class BlogPostWeekArchiveView(TemplateResponseMixin, ContextMixin, View):

	template_name = "blog/archive/week.html"

	def get(self, request, year, week, *args, **kwargs):
		try:
			date = datetime.date(*time.strptime("%s-0-%s" % (year, week), '%Y-%w-%U')[:3])
		except ValueError:
			raise Http404

		first_day = date
		last_day = date + datetime.timedelta(days=7)

		posts = Post.objects.archive_week(first_day, last_day).select_related()

		next_week = last_day + datetime.timedelta(days=1)
		prev_week = first_day + datetime.timedelta(days=-1)

		context = self.get_context_data()

		context = {
			'post_list': posts,
			'this_week': date,
			'next_week': next_week,
			'prev_week': prev_week,
		}

		return self.render_to_response(context)

class BlogPostDayArchiveView(TemplateResponseMixin, ContextMixin, View):

	template_name = "blog/archive/day.html"

	def get(self, request, year, month, day, *args, **kwargs):
		try:
			this_day = datetime.date(*time.strptime(year+month+day, '%Y%b%d')[:3])
		except ValueError:
			raise Http404

		next_day = this_day + datetime.timedelta(days=+1)
		prev_day = this_day - datetime.timedelta(days=-1)

		posts = Post.objects.archive_day(this_day).select_related()

		context = self.get_context_data()

		context = {
			'post_list': posts,
			'this_day': this_day,
			'next_day': next_day,
			'prev_day': prev_day,
		}

		return self.render_to_response(context)

class BlogPostUpdatedArchiveView(TemplateResponseMixin, ContextMixin, View):

	template_name = "blog/archive/updated.html"

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()

		context = {
			"post_list": Post.objects.updated()
		}

		return self.render_to_response(context)
