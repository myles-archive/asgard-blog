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

    template_name = 'blog/archive/archive.html'

    def get(self, request, **kwargs):
        posts = Post.objects.published()
        years = posts.dates('published', 'year')

        archive = {}

        for year in years:
            archive[year] = Post.objects.archvie_year(year).dates('published', 'month')

        context = self.get_context_data()

        context = {
            'archive': archive
        }

        return self.render_to_response(context)

class BlogPostYearArchiveView(TemplateResponseMixin, ContextMixin, View):

    template_name = "blog/archive/year.html"

    def get(self, request, year, *args, **kwargs):
        try:
            this_year = datetime.date(int(year), 1, 1)
        except ValueError:
            raise Http404

        posts = Post.objects.archvie_year(this_year).select_related()
        
        if not posts:
            raise Http404

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
        
        if not posts:
            raise Http404

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
        
        if not posts:
            raise Http404

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
        
        if not posts:
            raise Http404
        
        context = self.get_context_data()
        
        context = {
            'post_list': posts,
            'week_number': this_day.strftime("%U"),
            'this_day': this_day,
            'next_day': next_day,
            'prev_day': prev_day,
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
        
        if not posts:
            raise Http404

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
        
        posts = Post.objects.updated()
        
        if not posts:
            raise Http404

        context = {
            "post_list": posts
        }

        return self.render_to_response(context)
