from django.contrib import admin

from blog.models import Articles


@admin.register(Articles)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'contents', 'preview', 'is_published', 'published_by_whom')
