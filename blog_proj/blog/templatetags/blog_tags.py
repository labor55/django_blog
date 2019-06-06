from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count

# 使用模板标签，用于博客的侧边栏，使用simple_tag注册，
register = template.Library()
# 最新文章模板标签，获取数据库中前num篇文章，默认为5
@register.simple_tag
def get_recent_posts(num = 5):
    return Post.objects.all().order_by('-created_time')[:num]

# 归档模板标签，
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

# 分类模板标签
@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
