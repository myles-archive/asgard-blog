from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse

from asgard.tags.models import TaggedItem, Tag
from asgard.blog.models import Post, Category

class BlogPostFeed(Feed):
	_site = Site.objects.get_current()
	title = u"%s: latest weblog entries." % _site.name
	subtitle = u"More than a hapax legomenon."
	description_template = 'feeds/blog_post_description.html'
	
	def link(self):
		return reverse('blog_index')
	
	def items(self):
		return Post.objects.published()[:10]
	
	def item_link(self, item):
		return item.get_absolute_url() + "?utm_source=feedreader&utm_medium=feed&utm_campaign=BlogPostFeed"
	
	def item_pubdate(self, item):
		return item.published
	
	def item_updated(self, item):
		return item.date_modified
	
	def item_id(self, item):
		return item.get_absolute_url()
	
	def item_author_name(self, item):
		return u"%s %s" % (item.author.first_name, item.author.last_name)
	
	def item_author_email(self, item):
		return u"%s" % (item.author.email)
	
	def item_author_link(self, item):
		return reverse('blog_index')
	
	def item_categories(self, item):
		return item.tag_set.all()
	
	def item_copyright(self, item):
		return u"Copyright (c) %s, %s %s" % (self._site.name, item.author.first_name, item.author.last_name)
	
	def item_enclosure_url(self, item):
		return item.get_illustration_image()
	
	def feed_title(self):
		return u"%s" % _site.name
	
	def feed_authors(self):
		return ({"name": user.name} for user in User.objects.filter(is_staff=True))

class BlogCategoryPostFeed(Feed):
	_site = Site.objects.get_current()
	description_template = 'feeds/blog_post_description.html'
	
	def get_object(self, bits):
		slug = bits[0]
		return Category.objects.get(slug=slug)
	
	def title(self, obj):
		return u"%s: latest weblog entries for %s." % (self._site.name, obj.title)
	
	def subtitle(self, obj):
		return u"More than a hapax legomenon."
	
	def link(self, obj):
		return obj.get_absolute_url()
	
	def items(self, obj):
		return obj.post_set.all()
	
	def item_link(self, item):
		return item.get_absolute_url() + "?utm_source=feedreader&utm_medium=feed&utm_campaign=BlogCategoryPostFeed"
	
	def item_pubdate(self, item):
		return item.published
	
	def item_categories(self, item):
		return item.tag_set.all()

class BlogTagPostFeed(Feed):
	_site = Site.objects.get_current()
	description_template = 'feeds/blog_post_description.html'
	
	def get_object(self, bits):
		tag = bits[0]
		return Tag.objects.get(name=tag)
	
	def title(self, obj):
		return u"%s: latest weblog entries for %s." % (self._site.name, obj.name)
	
	def subtitle(self, obj):
		return u"More than a hapax legomenon."
	
	def link(self, obj):
		return reverse('blog_tags_detail', args=[obj.name,])
	
	def items(self, obj):
		return TaggedItem.objects.get_by_model(Post, obj)
	
	def item_link(self, item):
		return item.get_absolute_url() + "?utm_source=feedreader&utm_medium=feed&utm_campaign=BlogTagPostFeed"
	
	def item_pubdate(self, item):
		return item.published
	
	def item_categories(self, item):
		return item.tag_set.all()
