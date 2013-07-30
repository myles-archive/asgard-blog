from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.base import View, ContextMixin, TemplateResponseMixin

from blog.models import Post
from blog.settings import BLOG_PAGINATE_BY

__all__ = [
	'BlogPostAuthorListView',
	'BlogPostAuthorDetailView'
]

class BlogPostAuthorListView(TemplateResponseMixin, ContextMixin, View):
		
	template_name = "blog/author/list.html"

	def get(self, request, *args, **kwargs):

		users = User.objects.filter(is_staff=True)

		context = self.get_context_data(author_list=users)

		return self.render_to_response(context)

class BlogPostAuthorDetailView(TemplateResponseMixin, ContextMixin, View):

	template_name = "blog/author/detail.html"

	def get(self, request, username, page=1, count=BLOG_PAGINATE_BY, *args, **kwargs):
		try:
			author = User.objects.get(username__iexact=username)
		except User.DoesNotExist:
			raise Http404

		post_list = Post.objects.published(author=author)
		
		paginator = Paginator(post_list, int(request.GET.get('count', count)))
		
		try:
			posts = paginator.page(int(request.GET.get('page', page)))
		except (EmptyPage, InvalidPage):
			posts = paginator.page(paginator.num_pages)
		
		context = self.get_context_data(author=author, post_list=posts)

		return self.render_to_response(context)
