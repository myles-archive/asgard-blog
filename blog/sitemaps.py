from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from tagging.models import TaggedItem, Tag

from blog.models import Post, Category

class BlogPostSitemap(Sitemap):
	changefreq = "never"
	priority = 1.0
	
	def items(self):
		return Post.objects.published()
	
	def lastmod(self, obj):
		return obj.published

class BlogCategorySitemap(Sitemap):
	changefreq = "daily"
	priority = 0.1
	
	def items(self):
		return Category.objects.all()
	
	def lastmod(self, obj):
		try:
			post = obj.post_set.published()[0]
		except IndexError:
			return None
		return post.published
	
	def location(self, obj):
		return obj.get_absolute_url()

class BlogTagSitemap(Sitemap):
	changefreq = "daily"
	priority = 0.1
	
	def items(self):
		return Tag.objects.usage_for_model(Post)
	
	def lastmod(self, obj):
		try:
			post = TaggedItem.objects.get_by_model(Post, obj)[0]
		except IndexError:
			return None
		return post.published
	
	def location(self, obj):
		return reverse('blog_tags_detail', args=[obj.name,])
