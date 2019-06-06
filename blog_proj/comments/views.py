from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm
# Create your views here.
def post_comment(request, post_pk):
    # 获取被评论的文章，因为后面需要把评论和被评论的文章关联起来
    # 此函数是要么获取post，要么返回404页面（暂时不用）
    # post = get_object_or_404(Post, pk=post_pk)
    post = Post.objects.get(pk=post_pk)
    # 一般表单提交的是POST请求
    if request.method == 'POST':
        # 用户提交的数据在request.POST中
        form = CommentForm(request.POST)

        # 当调用form.is_valid()方法时，Django会自动帮我么检查表单的数据是否符合格式要求
        if form.is_valid():
            # 调用表单的save方法保存到数据库，但是仅仅生成模型实例，还没有保存到数据库
            comment = form.save(commit=False)
            # 将评论和被评论的文章关联起来
            comment.post = post
            # 最终将评论数据保存到数据库
            comment.save()
            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，
            # 它会调用这个模型实例的 get_absolute_url 方法，然后重定向至指定的url
            return redirect(post)

        else:
            # 检查到数据不合法， 重新渲染详情页， 并且渲染表单的错误
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            comment_list = post.comment_set.all()
            context = {'post':post,
                       'form':form,
                       'comment_list':comment_list}
            return render(request, 'blog/detail.html',context=context)

        # 非post请求，直接返回原detail页面
        return redirect(post)
