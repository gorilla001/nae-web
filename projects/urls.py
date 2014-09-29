from django.conf.urls import patterns,url

from projects import views

urlpatterns = patterns('',
    url(r'^$',views.index, name='index'),
    url(r'^\d+$',views.show, name='detail'),
    url(r'create/$',views.create, name='create'),
    url(r'delete/$',views.delete,name='delete'),
    url(r'detail/$',views.detail,name='show'),
    url(r'admin/$',views.admin,name='admin'),
)
