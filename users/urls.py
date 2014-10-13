from django.conf.urls import patterns,url

from users import views

urlpatterns = patterns('',
    url(r'^$',views.home, name='home'),
    url(r'^\d+$',views.show, name='detail'),
    url(r'create/$',views.create, name='create'),
    url(r'delete/$',views.delete,name='delete'),
    url(r'detail/$',views.detail,name='detail'),
    url(r'show/',views.show,name='show'),
    url(r'update/',views.update,name='update'),
    url(r'refresh/',views.refresh,name='refresh'),
    url(r'admin/$',views.admin,name='admin'),
    url(r'info/$',views.info,name='info'),
    url(r'index/$',views.index,name='index'),
)
