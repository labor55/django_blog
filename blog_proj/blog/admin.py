from django.contrib import admin
from blog.models import Post, Category, Tag

# Register your models here.
# @admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','modified_time','category','author']
    ordering = ['id']

admin.site.register(Category)
admin.site.register(Tag)

admin.site.register(Post,PostAdmin)
