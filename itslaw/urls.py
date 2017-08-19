from django.conf.urls import url
from . import views
app_name = 'itslaw'
urlpatterns = [

    url(r'^$', views.homepage, name='index'),

    ## 二级页面
    # 栏目组合页面
    url(r'^lanmu/(?P<lm_id>[0-9]+)/$', views.homepage, name='blog_lanmu'),
    # 分类的标签页面 - tag=column

]