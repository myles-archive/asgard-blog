from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist

from tagging.models import TaggedItem, Tag

from asgard.blog.models import Post, Category

current_site = Site.objects.get_current()

class BaseFeed(Feed):
	subtitle = u"More than a hapax legomenon."
	title_description = 'feeds/blog_post_title.html'
	description_template = 'feeds/blog_post_description.html'
	
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
		return reverse('blog_index') + "?utm_source=feedreader&utm_medium=feed&utm_campaign=BlogCategoryPostFeed"
	
	def item_categories(self, item):
		return item.tag_set.all()
	
	def item_copyright(self, item):
		return u"Copyright (c) %s, %s %s" % (current_site.name, item.author.first_name, item.author.last_name)
	
	def feed_title(self):
		return u"%s" % current_site.name
	
	def feed_authors(self):
		return ({"name": user.name} for user in User.objects.filter(is_staff=True))

class BlogPostFeed(BaseFeed):
	title = u"%s: weblog entries." % current_site.name
	
	def link(self):
		return reverse('blog_index') + "?utm_source=feedreader&utm_medium=feed&utm_campaign=BlogPostFeed"
	
	def items(self):
		return Post.objects.published()[:10]
	
	def item_link(self, item):
		return item.get_absolute_url() + "?utm_source=feedreader&utm_medium=feed&utm_campaign=BlogPostFeed"

class BlogCategoryPostFeed(BaseFeed):
	def get_object(self, bits):
		if len(bits) != 1:
			raise ObjectDoesNotExist
		return Category.objects.get(slug=bits[0])
	
	def title(self, obj):
		return u"%s: weblog entries categorized in %s." % (current_site.name, obj.title)
	
	def link(self, obj):
		return obj.get_absolute_url() + "?utm_source=feedreader&utm_medium=feed&utm_campaign=BlogCategoryPostFeed"
	
	def items(self, obj):
		return obj.post_set.all()
	
	def item_link(self, item):
		return item.get_absolute_url() + "?utm_source=feedreader&utm_medium=feed&utm_campaign=BlogCategoryPostFeed"

class BlogTagPostFeed(BaseFeed):
	def get_object(self, bits):
		if len(bits) != 1:
			raise ObjectDoesNotExist
		return Tag.objects.get(name=bits[0])
	
	def title(self, obj):
		return u"%s: weblog entries tagged in %s." % (current_site.name, obj.name)
	
	def link(self, obj):
		return reverse('blog_tags_detail', args=[obj.name,]) + "?utm_source=feedreader&utm_medium=feed&utm_campaign=BlogTagPostFeed"
	
	def items(self, obj):
		return TaggedItem.objects.get_by_model(Post, obj)
	
	def item_link(self, item):
		return item.get_absolute_url() + "?utm_source=feedreader&utm_medium=feed&utm_campaign=BlogTagPostFeed"