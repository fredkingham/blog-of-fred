from django.conf.urls.defaults import *
from blog import views

urlpatterns = patterns('',
    url(r'^$', views.BlogList.as_view(), name="blog_list"),
    url(r'^add/$', views.BlogCreate.as_view(), name='blog_create'),
    url(r'^post/(?P<slug>[-_\w]+)/edit/$', views.BlogUpdate.as_view(), name='blog_update'),
    url(r'^post/(?P<slug>[-_\w]+)/delete/$', views.BlogDelete.as_view(), name='blog_delete'),
    url(r'^post/(?P<slug>[-_\w]+)/$', views.BlogDetail.as_view(), name='blog_detail'),
)

