from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import BlogPost



@admin.register(BlogPost)
class BlogPostAdmin(MarkdownxModelAdmin):
    search_fields = ['title', 'content']
    readonly_fields = ['created', 'updated', 'created_by', 'views']
    prepopulated_fields = {'slug': ('title',), }

    list_filter = ['level', 'public', 'created_by', 'created']
    list_display = ['title', 'level', 'public', 'created_by', 'views', 'created']

    def save_model(self, request, obj, form, change):
            if not obj.pk:
                obj.created_by = request.user
            super().save_model(request, obj, form, change)


