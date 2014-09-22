from django.conf.urls import patterns,url

import views

urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
    url(r'projects/$',views.projects,name='projects'),
    url(r'images/$',views.images,name='images'),
    url(r'images/create/$',views.createImage,name='create'),
    url(r'files/$',views.files,name='files'),
    url(r'files/create/$',views.createFile,name='create'),
    url(r'files/show/$',views.showFile,name="show"),
    url(r'files/delete/$',views.deleteFile,name="delete"),
    url(r'users/$',views.users,name='users'),
    url(r'users/create/$',views.createUser,name='users'),
)
