from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.base import View, ContextMixin, TemplateResponseMixin

from blog.models import Post
from blog.settings import BLOG_PAGINATE_BY

__all__ = [
	'BlogTagListView', 'BlogTagDetailView'
]

class BlogTagListView(TemplateResponseMixin, ContextMixin, View):

	template_name = 'blog/tag/list.html'

	def get(self, request, *args, **kwargs):
		tags = Post.tags.all()

		context = self.get_context_data(tag_list=tags)
		
		return self.render_to_response(context)

class BlogTagDetailView(TemplateResponseMixin, ContextMixin, View):

	template_name = 'blog/tag/detail.html'

	def get(self, request, slug, page=1, count=BLOG_PAGINATE_BY, *args, **kwargs):

		tag = Post.tags.get(slug=slug)

		post_list = Post.objects.filter(tags__in=[tag]).select_related()

		paginator = Paginator(post_list, int(request.GET.get('count', count)))

		try:
			posts = paginator.page(int(request.GET.get('page', page)))
		except (EmptyPage, InvalidPage):
			posts = paginator.page(paginator.num_pages)

		context = self.get_context_data()

		context = {
			'tag': tag,
			'post_list': posts,
		}

		return self.render_to_response(context)