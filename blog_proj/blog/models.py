from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
import markdown
from django.utils.html import strip_tags

# Create your models here.
# 兼容python2
@python_2_unicode_compatible
class Category(models.Model):
    # 博客分类
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):
    # 博客标签
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model):
    # 这个是文章数据库表

    # 文章标题
    title = models.CharField(max_length=70)

    # 文章正文 用TextField存储
    body = models.TextField()

    # 文章创建时间和更改时间
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要，默认可以为空（CharField()要求必须要填入数据）
    excerpt = models.CharField(max_length=200, blank=True)

    # 与分类建立一对多的关系，使用外键，即一篇文章只能对应一个分类
    # 与标签建立多对多的关系，即一篇文章可对应多个标签，一个标签也可关联多篇文章
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    # 一篇文章只能对应一个作者，但是一个作者可以写多篇文章
    author = models.ForeignKey(User)
    # 阅读量
    read = models.IntegerField(default=0)
    def __str__(self):
        return self.title
    # 反解析，点击之后就到detail.html文件中，并传递一个PK参数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']

    # 自动保存摘要
    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 渲染成md文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                ])

            # 就将正文的前54个字符设置为摘要
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)
