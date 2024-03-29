from django.db import models
from django.utils.six import python_2_unicode_compatible
# Create your models here.
# 创建一个评论应用的数据库
@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Post')
    def __str__(self):
        return self.text[:20]
