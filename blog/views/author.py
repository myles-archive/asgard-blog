from django.views.generic import ListView
from django.contrib.auth.models import User

from blog.models import Post
from blog.settings import BLOG_PAGINATE_BY

__all__ = [
	'BlogPostAuthorListView',
	'BlogPostAuthorDetailView'
]

class BlogPostAuthorListView(ListView):
	
	context_object_name = "authors"
	template_name = "blog/author/list.html"
	
	def get_queryset(self):
		return User.objects.filter(is_staff=True)

class BlogPostAuthorDetailView(ListView):
	
	context_object_name = "post_list"
	template_name = "blog/author/detail.html"
	paginate_by = BLOG_PAGINATE_BY
	
	def get_context_data(self, **kwargs):
		context = super(BlogPostAuthorDetailView, self).get_context_data(**kwargs)
		context['author'] = self.author
		return context
	
	def get_queryset(self):
		self.author = User.objects.get(username__iexact=self.kwargs['username'])
		return Post.objects.published(author=self.author)