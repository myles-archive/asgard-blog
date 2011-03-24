from datetime import datetime
import operator

from django.db.models import Manager, Q

class PostManager(Manager):
	"""
	Same as above but for templates
	"""
	def get_query_set(self):
		return super(PostManager, self).get_query_set()
	
	def published(self, **kwargs):
		"""Returns a list of published blog posts which status is 'Public' and
		the published date and time is less than today.
		"""
		return self.get_query_set().filter(status__gte=2,
			published__lte=datetime.now(), **kwargs)
	
	def public(self, **kwargs):
		"""Returns a list of public blog posts which status is 'Public'
		"""
		return self.get_query_set().filter(status__gte=2, **kwargs)
	
	def updated(self, **kwargs):
		"""Returns a list of blog posts which have been updated."""
		return self.published(**kwargs).extra(where=['date_modified > published']).order_by('-date_modified')
	
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
