from django import forms
from .models import Comment

# 表单提交
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment  # 表示此表单对应的数据库是Comment
        # 表单要显示的字段
        fields = ['name', 'email', 'url', 'text']
