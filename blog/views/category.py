from django.http import Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.base import View, ContextMixin, TemplateResponseMixin

from blog.models import Post, Category
from blog.settings import BLOG_PAGINATE_BY

__all__ = [
	'BlogCategoryDetailView',
	'BlogCategoryListView'
]

class BlogCategoryListView(TemplateResponseMixin, ContextMixin, View):

	template_name = "blog/category/list.html"

	def get(self, request, *args, **kwargs):
		categories = Category.objects.all().select_related()

		context = self.get_context_data(category_list=categories)
		
		return self.render_to_response(context)

class BlogCategoryDetailView(TemplateResponseMixin, ContextMixin, View):
	
	template_name = "blog/category/detail.html"

	def get(self, request, slug, page=1, count=BLOG_PAGINATE_BY, *args, **kwargs):
		try:
			category = Category.objects.get(slug__iexact=slug)
		except Category.DoesNotExist:
			raise Http404

		posts = Post.objects.published(categories=category)

		context = self.get_context_data(category=category, post_list=posts)

		return self.render_to_response(context)
