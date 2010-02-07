from django.contrib import admin
from blog.models import Post, Category

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'published', 'status_boolean', '_get_tags', '_get_categories',)
	list_filter = ('published', 'status',)
	filter_horizontal = ('categories',)
	prepopulated_fields = {'slug': ('title',)}
	date_hierarchy = 'published'
	search_field = ('title', 'body')
	fieldsets = (
		(None, {
			'fields': (
				('title', 'slug'),
				'body', 'body_markup_choices', 'tease', 'tags', 'published', 'author', 'status'),
		}),
		('Advanced options', {
			'classes': ('collapse',),
			'fields': ('allow_comments', 'allow_pings', 'send_pings', 'categories')
		})
	)
	
	def save_model(self, request, obj, form, change):
		if not obj.author:
			obj.author = request.user
		
		obj.save()

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = { 'slug': ('title',) }

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
