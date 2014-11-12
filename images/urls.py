from django.conf.urls import patterns,url

from  images import views

urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
    url(r'create/$',views.create,name='create'),
    url(r'delete/$',views.delete,name="delete"),
    url(r'show/$',views.show,name='show'),
    url(r'update/$',views.update,name="update"),
    url(r'edit/$',views.edit,name="edit"),
    url(r'commit/$',views.commit,name="commit"),
    url(r'conflict/$',views.conflict,name="conflict"),
)
