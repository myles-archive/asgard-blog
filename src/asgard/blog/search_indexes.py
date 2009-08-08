from haystack import site, indexes

from asgard.blog.models import Post

class PostIndex(indexes.SearchIndex):
	text = indexes.CharField(document=True, use_template=True)
	published = indexes.DateTimeField(model_attr='published')
	
	def get_query_set(self):
		return Post.objects.published()

site.register(Post, PostIndex)