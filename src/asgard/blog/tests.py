"""
Copyright (C) 2008 Myles Braithwaite

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
	
	http://www.apache.org/licenses/LICENSE-2.0
	
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import unittest
import datetime

from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings

from asgard.blog.models import Post, Category
from asgard.blog.templatetags import blog_tags
from asgard.tags.models import Tag

from django.test import TestCase

client = Client()

class BlogTestCase(TestCase):
	fixtures = ['blog',]
	
	def setUp(self):
		self.post = Post.objects.get(pk=1)
		self.category = Category.objects.get(pk=1)
	
	def testPostDigitalFingerprint(self):
		self.assertEquals(self.post.digital_fingerprint, 'c974b23eabea866720a6fc1963a6c727')
	
	def testCategory(self):
		self.post.categories.add(self.category)
		self.post.save()
	
	def testBlogIndex(self):
		response = client.get(reverse('blog_index'))
		self.assertEquals(response.status_code, 200)
	
	def testPostDetailThoughModel(self):
		response = client.get(self.post.get_absolute_url())
		self.assertEquals(response.status_code, 200)
	
	def testPostDetailThoughURL(self):
		year = self.post.published.year
		month = self.post.published.strftime('%b').lower()
		day = self.post.published.day
		slug = self.post.slug
		response = client.get(reverse('blog_post_detail', args=[year, month, day, slug,]))
		self.assertEquals(response.status_code, 200)
	
	def testCategoryList(self):
		response = client.get(reverse('blog_categories_list'))
		self.assertEquals(response.status_code, 200)
	
	def testCategoryDetail(self):
		response = client.get(self.category.get_absolute_url())
		self.assertEquals(response.status_code, 200)
	
	def testTagList(self):
		response = client.get(reverse('blog_tags_list'))
		self.assertEquals(response.status_code, 200)
	
	def testTagDetail(self):
		tag = Tag.objects.get_for_object(self.post)[0]
		response = client.get(reverse('blog_tags_detail', args=[tag.name,]))
		self.assertEquals(response.status_code, 200)
	
	def testPostYear(self):
		year = self.post.published.year
		response = client.get(reverse('blog_archive_year', args=[year,]))
		self.assertEquals(response.status_code, 200)
	
	def testPostMonth(self):
		year = self.post.published.year
		month = self.post.published.strftime('%b').lower()
		response = client.get(reverse('blog_archive_month', args=[year, month,]))
		self.assertEquals(response.status_code, 200)
	
	def testPostDay(self):
		year = self.post.published.year
		month = self.post.published.strftime('%b').lower()
		day = self.post.published.day
		response = client.get(reverse('blog_archive_day', args=[year, month, day,]))
		self.assertEquals(response.status_code, 200)
	
	def testTemplateTagGetLinks(self):
		links = blog_tags.get_links(self.post.body)
		self.assertEquals('<a href="http://example.org/">Lorem ipsum</a>', str(links[0]))
	
	def testBlogSearchPage(self):
		response = client.get(reverse('blog_search'))
		self.assertEquals(response.status_code, 200)
	
	def testBlogSearchQuery(self):
		response = client.get(reverse('blog_search'), {"q": "lorem"})
		self.assertEquals(response.status_code, 200)
