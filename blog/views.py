import datetime, time, re

from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from tagging.views import tagged_object_list

from blog.models import Post, Category
from blog.forms import STOP_WORDS, BlogSearchForm

def index(request, page=1, context={}, template_name='blog/index.html'):
	"""
	Blog index page.
	"""
	post_list = Post.objects.published().select_related()
	paginator = Paginator(post_list, 5)
	
	try:
		posts = paginator.page(page)
	except (EmptyPage, InvalidPage):
		posts = paginator.page(paginator.num_pages)
	
	context.update({
		'posts': posts,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def archive(request, context={}, template_name='blog/archive.html'):
	posts = Post.objects.published()
	years = posts.dates('published', 'year')
	months = posts.dates('published', 'month')
	
	context.update({
		'years': years,
		'months': months,
		'is_archive': True,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def archive_year(request, year, page=1, context={}, template_name='blog/archive_year.html'):
	posts = Post.objects.public(published__year=year).select_related()
	
	this_year = datetime.date(int(year), 1, 1)
	next_year = this_year + datetime.timedelta(days=+366)
	prev_year = this_year + datetime.timedelta(days=-365)
	
	context.update({
		'posts': posts,
		'this_year': this_year,
		'next_year': next_year,
		'prev_year': prev_year,
		'is_archive': True,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def archive_month(request, year, month, page=1, context={}, template_name='blog/archive_month.html'):
	try:
		date = datetime.date(*time.strptime(year+month, '%Y%b')[:3])
	except ValueError:
		raise Http404
	
	first_day = date.replace(day=1)
	if first_day.month == 12:
		last_day = first_day.replace(year=first_day.year + 1, month=1)
	else:
		last_day = first_day.replace(month=first_day.month + 1)
	
	next_month = last_day + datetime.timedelta(days=1)
	prev_month = first_day - datetime.timedelta(days=-1)
	
	posts = Post.objects.public(published__gte=first_day, published__lt=last_day).select_related()
	
	context.update({
		'posts': posts,
		'this_month': date,
		'next_month': next_month,
		'prev_month': prev_month,
		'is_archive': True,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def archive_day(request, year, month, day, page=1, context={}, template_name='blog/archive_day.html'):
	try:
		date = datetime.date(*time.strptime(year+month+day, '%Y%b%d')[:3])
	except ValueError:
		raise Http404
	
	next_day = date + datetime.timedelta(days=+1)
	prev_day = date - datetime.timedelta(days=-1)
	
	posts = Post.objects.public(published__range=(datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max))).select_related()
	
	context.update({
		'posts': posts,
		'this_day': date,
		'next_day': next_day,
		'prev_day': prev_day,
		'is_archive': True,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def detail(request, year, month, day, slug, context={}, template_name='blog/detail.html'):
	try:
		date = datetime.date(*time.strptime(year+month+day, '%Y%b%d')[:3])
	except ValueError:
		raise Http404
	
	try:
		# post = Post.objects.public(published__range=(datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max)), slug__iexact=slug).select_related()[0]
		post = Post.objects.select_related().get(published__range=(datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max)), slug__iexact=slug)
	except Post.DoesNotExist:
		raise Http404
	
	context.update({
		'post': post,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def category_list(request, context={}, template_name='blog/category_list.html'):
	categories = Category.objects.all()
	
	context.update({
		'categories': categories,
		'is_archive': True,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def category_detail(request, slug, page=1, context={}, template_name='blog/category_detail.html'):
	try:
		category = Category.objects.get(slug__iexact=slug)
	except Category.DoesNotExist:
		raise Http404
	
	posts = Post.objects.published(categories=category)
	
	context.update({
		'category': category,
		'posts': posts,
		'is_archive': True,
	})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def tag_list(request, context={}, template_name='blog/tag_list.html'):
	context.update({
		'is_archive': True,
	})
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def tag_detail(request, tag, page=1, context={}, template_name='blog/tag_detail.html'):
	context.update({
		'is_archive': True,
	})
	queryset = Post.objects.all()
	return tagged_object_list(request, queryset, tag, paginate_by=25, allow_empty=True, template_name=template_name)

def search(request, context={}, template_name='blog/search.html'):
	new_data = request.GET.copy()
	form = BlogSearchForm(new_data)
	if form.is_valid():
		stop_word_list = re.compile(STOP_WORDS, re.IGNORECASE)
		search_term = form.cleaned_data['q']
		cleaned_search_term = stop_word_list.sub('', search_term)
		if cleaned_search_term:
			query = Post.objects.search(cleaned_search_term.strip())
		else:
			query = None
		
		context.update({
			'results': query,
			'query': form.cleaned_data['q'],
			'form': form,
			'is_archive': True,
		})
	else:
		form = BlogSearchForm()
		context.update({
			'form': form,
			'is_archive': True,
		})
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))
