import re

from django.views.generic import ListView

from blog.models import Post
from blog.settings import BLOG_PAGINATE_BY
from blog.forms import STOP_WORDS, BlogSearchForm

__all__ = [
	'BlogPostSearchFormListView',
]

class BlogPostSearchFormListView(ListView):
	
	context_object_name = "post_list"
	template_name = "blog/search.html"
	# paginate_by = BLOG_PAGINATE_BY
	allow_empty = True
	
	def get_queryset(self):
		self.new_data = self.request.GET.copy()
		self.form = BlogSearchForm(self.new_data)
		if self.form.is_valid():
			stop_word_list = re.compile(STOP_WORDS, re.IGNORECASE)
			search_term = self.form.cleaned_data['q']
			cleaned_search_term = stop_word_list.sub('', search_term)
			if cleaned_search_term:
				return Post.objects.search(cleaned_search_term.strip())
			else:
				return []
	
	def get_context_data(self, **kwargs):
		context = super(BlogPostSearchFormListView, self).get_context_data(**kwargs)
		context['form'] = self.form
		try:
			context['query'] = self.form.cleaned_data.get('q', None)
		except AttributeError:
			context['query'] = None
		return context