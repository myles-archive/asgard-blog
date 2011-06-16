import datetime
import operator

from django.db.models import Manager, Q

from blog.settings import BLOG_MULTIPLE_SITES

if BLOG_MULTIPLE_SITES:
	from django.contrib.sites.models import Site
	current_site = Site.objects.get_current()
else:
	current_site = None

class PostManager(Manager):
	"""
	Same as above but for templates
	"""
	def get_query_set(self):
		if current_site:
			return super(PostManager, self).get_query_set().filter(sites__in=[current_site,])
		else:
			return super(PostManager, self).get_query_set()
	
	def published(self, **kwargs):
		"""Returns a list of published blog posts which status is 'Public' and
		the published date and time is less than today.
		"""
		return self.get_query_set().filter(status__gte=2,
			published__lte=datetime.datetime.now(), **kwargs)
	
	def public(self, **kwargs):
		"""Returns a list of public blog posts which status is 'Public'
		"""
		return self.get_query_set().filter(status__gte=2, **kwargs)
	
	def updated(self, **kwargs):
		"""Returns a list of blog posts which have been updated."""
		return self.published(**kwargs).extra(where=['date_modified > published']).order_by('-date_modified')
	
	def archvie_year(self, date, **kwargs):
		"""Returns a list of blog posts for a given year."""
		return self.public(published__year=date.year)
	
	def archive_month(self, date, **kwargs):
		"""Returns a list of blog posts for a given month."""
		return self.public(published__month=date.month, published__year=date.year)
	
	def archive_day(self, date, **kwargs):
		"""Returns a list of blog posts for a given day."""
		return self.public(published__day=date.day, published__month=date.month, published__year=date.year)
	
	def get_post(self, slug, date=None, **kwargs):
		"""Returns a blog post.
		
		:arg slug: The slug of the blog post.
		:arg date: The date the blog post was published.
		"""
		if date:
			return self.get(published__range=(datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max)), slug__iexact=slug)
		else:
			return self.get(slug__iexact=slug)
	
	def search(self, search_terms):
		"""Search the current published blog posts for a term in the title and
		body field.
		
		:arg search_terms: The term you wish to search for.
		"""
		terms = [term.strip() for term in search_terms.split()]
		q_objects = []
	
		for term in terms:
			q_objects.append(Q(title__icontains=term))
			q_objects.append(Q(body__icontains=term))
	
		qs = self.published()
		return qs.filter(reduce(operator.or_, q_objects))
