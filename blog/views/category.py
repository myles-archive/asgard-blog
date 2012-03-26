from django.views.generic import ListView

from blog.models import Post, Category
from blog.settings import BLOG_PAGINATE_BY

__all__ = [
	'BlogCategoryDetailView',
	'BlogCategoryListView'
]

class BlogCategoryListView(ListView):
	
	context_object_name = "category_list"
	template_name = "blog/category/list.html"
	
	def get_queryset(self):
		return Category.objects.all().select_related()

class BlogCategoryDetailView(ListView):
	
	context_object_name = 'posts'
	template_name = "blog/category/detail.html"
	paginate_by = BLOG_PAGINATE_BY
	
	def get_queryset(self):
		try:
			self.category = Category.objects.get(slug__iexact=self.kwargs['slug'])
		except Category.DoesNotExist:
			raise Http404
		
		return Post.objects.published(categories=self.category)