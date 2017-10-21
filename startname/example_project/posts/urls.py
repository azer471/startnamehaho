from __future__ import unicode_literals
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView



app_name = 'posts'

urlpatterns = [
	# /portada/
    url(r'^$', views.index, name ='index'),

    # /portada/71/
    url (r'^(?P<article_id>[0-9]+)/$', views.detail, name ='detail'),

        # ex: /posts/5/vote/
    url(r'^(?P<article_id>[0-9]+)/vote/$', views.vote, name='vote'),
#posts/article/add

	url(r'^article/add/$', views.post_new, name='article-create'),

#for User
	url(r'^register/$', views.UserFormView.as_view(), name='register'),
	url(r'^login/$', auth_views.login, {'template_name': 'posts/login.html'}, name='login'),

    url(r'^accounts/(?P<username>[a-zA-Z0-9]+)$', views.profile, name='user_profile'),
 #   url(r'^accounts/profile/(?P<username>[\w.@+-]+)/$', views.profile, name='user_profile'),

    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    ]














#urlpatterns = [
#    url(r'^$',views.post_list, name ='post_list'),
#    url(r'^create/$',"posts.views.post_create"),
#    url(r'^detail/$',"posts.views.post_detail"),
#    url(r'^update/$',"posts.views.post_update"),
#    url(r'^delete/$',"posts.views.post_delete"),
#]
