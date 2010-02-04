from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic

from tagging import register as tags_register
from tagging.fields import TagField

from blog.managers import ManagerWithPublished

from asgard.utils.db.fields import MarkupTextField

# from related.models import RelatedLink, RelatedObject

class Category(models.Model):
	title = models.CharField(_('title'), max_length=200)
	slug = models.SlugField(_('slug'), max_length=25)
	date_added = models.DateTimeField(_('date added'), auto_now_add=True)
	date_modified = models.DateTimeField(_('date modified'), auto_now=True)
	
	class Meta:
		verbose_name = _('category')
		verbose_name_plural = _('categories')
		db_table = 'blog_categories'
		ordering = ('title',)
	
	def __unicode__(self):
		return u"%s" % self.title
	
	@permalink
	def get_absolute_url(self):
		return ('blog_categories_detail', None, {
			'slug': self.slug,
		})

class Post(models.Model):
	"""
	Post model.
	"""
	STATUS_CHOICES = (
		(1, 'Draft'),
		(2, 'Public')
	)
	title = models.CharField(_('title'), max_length=200)
	slug = models.SlugField(_('slug'), max_length=50)
	author = models.ForeignKey(User)
	status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=1)
	
	categories = models.ManyToManyField(Category, blank=True, null=True)
	tags = TagField()
	
	tease = models.TextField(_('tease'), blank=True, null=True)
	
	body = MarkupTextField(_('body'))
	
	allow_pings = models.BooleanField(_('Allow Pings'), default=True)
	send_pings = models.BooleanField(_('Send Pings'), default=True)
	allow_comments = models.BooleanField(_('Allow Comments'), default=True)
	
	published = models.DateTimeField(_('published'), blank=True, null=True)
	date_added = models.DateTimeField(_('date added'), auto_now_add=True)
	date_modified = models.DateTimeField(_('date modified'), auto_now=True)
	
	comments = generic.GenericRelation(Comment, object_id_field='object_pk')
	# related_links = generic.GenericRelation(RelatedLink)
	# related_objects = generic.GenericRelation(RelatedObject)
	
	objects = ManagerWithPublished()
	
	class Meta:
		verbose_name = _('post')
		verbose_name_plural = _('posts')
		db_table = 'blog_posts'
		unique_together = ('slug', 'published')
		get_latest_by = 'published'
		ordering = ('-published', '-date_added')
	
	def __unicode__(self):
		return u"%s" % self.title
	
	@permalink
	def get_absolute_url(self):
		return ('blog_post_detail', None, {
			'year': str(self.published.year),
			'month': self.published.strftime('%b').lower(),
			'day': str(self.published.day),
			'slug': self.slug,
		})
	
	@property
	def get_next_post(self):
		next = Post.objects.filter(**{'published__gt': self.pub_date}).order_by('published')
		try:
			return next[0]
		except IndexError:
			return None
	
	@property
	def get_previous_post(self):
		previous = Post.objects.filter(**{'published__lt': self.pub_date}).order_by('-published')
		try:
			return previous[0]
		except IndexError:
			return None
	
	@property
	def digital_fingerprint(self):
		try:
			from hashlib import md5
			return md5(self.title).hexdigest()
		except ImportError:
			import md5
			return md5.new(self.title).hexdigest()
	
	def _get_comment_count(self):
		return u"%s" % self.comments.count()
	
	_get_comment_count.short_description = _("Number of Comments")
	
	def status_boolean(self):
		if self.published:
			if self.status == 2:
				return True
			else:
				return False
		else:
			return False
	
	status_boolean.short_description = _("Status")
	status_boolean.boolean = True
	
	def _get_tags(self):
		tag_string = ''
		for t in self.tag_set.all():
			link = '<a href="./?tags__id__exact=%s" title="Show all post under %s tag">%s</a>' % (t.id, t.name, t.name)
			link = u"%s" % t.name
			tag_string = ''.join([tag_string, link, ', '])
		return tag_string.rstrip(', ')
	
	_get_tags.short_description = _('Tags')
	_get_tags.allow_tags = True
	
	def _get_categories(self):
		category_string = ''
		for c in self.categories.all():
			link = '<a href="./?categories__id__exact=%s" title="Show all post under %s category">%s</a>' % (c.id, c.title, c.title)
			category_string = ''.join([category_string, link, ', '])
		return category_string.rstrip(', ')
	
	_get_categories.short_description = _('Categories')
	_get_categories.allow_tags = True

tags_register(Post, 'tag_set')
