from django.conf.urls import patterns,url

import views

urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
    url(r'projects/$',views.projects,name='projects'),
    url(r'images/$',views.images,name='images'),
    url(r'files/$',views.files,name='files'),
    url(r'users/$',views.users,name='users'),
)
