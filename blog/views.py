from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blog.models import Post, Category, Tag
from django.core.paginator import Paginator
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
# Create your views here.

# blog主页
def index(request):
    post_list = Post.objects.all()
    # 分页 每页显示2条
    p = Paginator(post_list,2)
    # 得到点击的值，默认为1
    page_num = request.GET.get('page',1)
    now_num = int(page_num)
    # 获取页面内容
    page = p.page(now_num)

    return render(request,'blog/index.html',context={'page':page})

# 每条博客的内容
def detail(request, pk):
    # 获取项目
    post = Post.objects.get(pk=pk)
    # post = get_object_or_404(Post, pk=pk)
    # 启用markdown编辑器
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ])

    form = CommentForm()
    # 获取这篇blog的所有评论
    comment_list = post.comment_set.all()
    context = {'post':post,
               'form':form,
               'comment_list':comment_list
               }
    # 设置阅读数量
    response = render(request, 'blog/detail.html', context= context)
    if not request.COOKIES.get('read{}'.format(pk)):
        post.read += 1
        post.save()
        response.set_cookie('read{}'.format(pk),1,60)
    return response

# 父模板
def base(request):
    return render(request, 'blog/base.html')

# 归档函数,修改超链接部分
def archives(request, year, month):
    post_list = Post.objects.filter(
        created_time__year=year,
        created_time__month=month
    )
    return render(request, 'blog/index.html', context={'post_list':post_list})

# 分类函数
def category(request, pk):
    # cate = get_object_or_404(Category, pk=pk)
    cate = Category.objects.get(pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list':post_list})

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)
