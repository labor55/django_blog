from django.conf.urls import url
from blog import views

# 本urls.py是属于blog应用的
app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    # 设置url的name，以便在model可以找到此url
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^base/$', views.base, name='base'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})$', views.archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
]
