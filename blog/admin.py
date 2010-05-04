from django.contrib import admin
from blog.models import Post, Category
from django.utils.translation import ugettext_lazy as _

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'published', 'status_boolean', 'allow_pings', 'allow_comments', '_get_tags', '_get_categories',)
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
	
	actions = ['make_published', 'make_draft', 'close_comments_pings']
	
	def make_published(self, request, queryset):
		queryset.update(status=2)
	
	make_published.short_description = _('Mark selected posts as Published')
	
	def make_draft(self, request, queryset):
		queryset.update(status=1)
	
	make_draft.short_description = _('Mark selected posts as Drafts')
	
	def close_comments_pings(self, request, queryset):
		queryset.update(allow_comments=False, allow_pings=False)
	
	close_comments_pings.short_description = _('Close comments & pings on selected posts')
	
	def get_actions(self, request):
		actions = super(PostAdmin, self).get_actions(request)
		
		if not request.user.is_superuser:
			del actions['delete_selected']
		
		return actions
	
	def save_model(self, request, obj, form, change):
		if not obj.author:
			obj.author = request.user
		
		obj.save()

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = { 'slug': ('title',) }

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
