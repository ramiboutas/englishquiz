from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import BlogPost



@admin.register(BlogPost)
class BlogPostAdmin(MarkdownxModelAdmin):
    readonly_fields = ['created', 'updated', 'author']
    prepopulated_fields = {'slug': ('title',), }
    def save_model(self, request, obj, form, change):
            if not obj.pk:
                obj.created_by = request.user
            super().save_model(request, obj, form, change)




#admin.site.register(Post, MarkdownxModelAdmin)