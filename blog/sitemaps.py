from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from blog.models import Post, Category

class BlogPostSitemap(Sitemap):
	changefreq = "never"
	priority = 1.0
	
	def items(self):
		return Post.objects.published()
	
	def lastmod(self, obj):
		return obj.published

class BlogCategorySitemap(Sitemap):
	changefreq = "monthly"
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
	changefreq = "weekly"
	priority = 0.1
	
	def items(self):
		return Post.tags.all()
	
	def location(self, obj):
		return reverse('blog_tags_detail', args=[obj.slug,])
