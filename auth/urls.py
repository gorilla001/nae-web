from django.conf.urls import patterns,url
from auth import views

urlpatterns = patterns('',
    url(r'^$',views.auth_login,name='auth')
)
