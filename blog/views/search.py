import re

from django.http import Http404

from django.views.generic.base import View, ContextMixin, TemplateResponseMixin


from blog.models import Post
from blog.settings import BLOG_PAGINATE_BY
from blog.forms import STOP_WORDS, BlogSearchForm

__all__ = [
	'BlogPostSearchFormListView',
]

class BlogPostSearchFormListView(TemplateResponseMixin, ContextMixin, View):
	
	template_name = "blog/search.html"

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()

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

			context = {
				'results': query,
				'query': form.cleaned_data['q'],
				'form': form,
			}
		else:
			form = BlogSearchForm()
			context = {
				'form': form,
			}

		return self.render_to_response(context)
