from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse

from blog.models import Post, Category
from blog.templatetags import blog_tags

class BlogTestCase(TestCase):
	fixtures = ['auth', 'blog',]
	
	def setUp(self):
		self.post = Post.objects.get(pk=1)
		self.post.tags.add('lorem-ipsum')
		self.post.save()
		self.category = Category.objects.get(pk=1)
		self.client = Client()
	
	def testPostDigitalFingerprint(self):
		self.assertEquals(self.post.digital_fingerprint, 'c974b23eabea866720a6fc1963a6c727')
	
	def testCategory(self):
		self.post.categories.add(self.category)
		self.post.save()
	
	def testBlogIndex(self):
		response = self.client.get(reverse('blog_index'))
		self.assertEquals(response.status_code, 200)
	
	def testPostDetailThoughModel(self):
		response = self.client.get(self.post.get_absolute_url())
		self.assertEquals(response.status_code, 200)
	
	def testPostDetailThoughURL(self):
		year = self.post.published.year
		month = self.post.published.strftime('%b').lower()
		day = self.post.published.day
		slug = self.post.slug
		response = self.client.get(reverse('blog_post_detail', args=[year, month, day, slug,]))
		self.assertEquals(response.status_code, 200)
	
	def testCategoryList(self):
		response = self.client.get(reverse('blog_categories_list'))
		self.assertEquals(response.status_code, 200)
	
	def testCategoryDetail(self):
		response = self.client.get(self.category.get_absolute_url())
		self.assertEquals(response.status_code, 200)
	
	def testTagList(self):
		response = self.client.get(reverse('blog_tags_list'))
		self.assertEquals(response.status_code, 200)
	
	def testTagDetail(self):
		tag = self.post.tags.all()[0]
		response = self.client.get(reverse('blog_tags_detail', args=[tag.slug,]))
		self.assertEquals(response.status_code, 200)
	
	def testAuthorList(self):
		response = self.client.get(reverse('blog_authors_list'))
		self.assertEquals(response.status_code, 200)
	
	def testAuthorDetail(self):
		response = self.client.get(reverse('blog_authors_detail', args=['myles',]))
		self.assertEquals(response.status_code, 200)
	
	def testPostYear(self):
		year = self.post.published.year
		response = self.client.get(reverse('blog_archive_year', args=[year,]))
		self.assertEquals(response.status_code, 200)
	
	def testPostMonth(self):
		year = self.post.published.year
		month = self.post.published.strftime('%b').lower()
		response = self.client.get(reverse('blog_archive_month', args=[year, month,]))
		self.assertEquals(response.status_code, 200)
	
	def testPostDay(self):
		year = self.post.published.year
		month = self.post.published.strftime('%b').lower()
		day = self.post.published.day
		response = self.client.get(reverse('blog_archive_day', args=[year, month, day,]))
		self.assertEquals(response.status_code, 200)
	
	def testTemplateTagGetLinks(self):
		links = blog_tags.get_links(self.post.body)
		self.assertEquals('<a href="http://example.org/">Lorem ipsum</a>', str(links[0]))
	
	def testTempalteTagGetLatestPosts(self):
		context = {}
		posts = blog_tags.LatestPosts(1, 'posts').render(context)
		self.assertTrue(context['posts'])
		self.assertEqual(posts, '')
	
	def testTemplateTagBlogCategories(self):
		context = {}
		categories = blog_tags.BlogCategories('categories').render(context)
		self.assertTrue(context['categories'])
		self.assertEqual(categories, '')
	
	def testTemplateTagStripIllustrations(self):
		text = """<p class="illustration"><img /> A caption.</p><p>This should remain</p>"""
		striped_text = blog_tags.strip_illustrations(text)
		self.assertEqual(striped_text, '<p>This should remain</p>')
	
	def testBlogSearchPage(self):
		response = self.client.get(reverse('blog_search'))
		self.assertEquals(response.status_code, 200)
	
	def testBlogSearchQuery(self):
		response = self.client.get(reverse('blog_search'), {"q": "lorem"})
		self.assertEquals(response.status_code, 200)
	
	def testBlogSitemaps(self):
		response = self.client.get(reverse('sitemap'))
		self.assertEquals(response.status_code, 200)
	
	def testBlogPostFeed(self):
		response = self.client.get(reverse('blog_post_feed'))
		self.assertEquals(response.status_code, 200)
	
	def testBlogCategoryPostFeed(self):
		response = self.client.get(reverse('blog_category_post_feed', args=['lorem-ipsum']))
		self.assertEquals(response.status_code, 200)
	
	def testBlogTagPostFeed(self):
		response = self.client.get(reverse('blog_tag_post_feed', args=['lorem-ipsum']))
		self.assertEquals(response.status_code, 200)
	
	def testBlogAuthorPostFeed(self):
		response = self.client.get(reverse('blog_author_post_feed', args=['myles']))
		self.assertEquals(response.status_code, 200)

