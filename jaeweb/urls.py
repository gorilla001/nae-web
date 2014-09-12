from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

import overview.urls
import containers.urls
import images.urls
import codeversion.urls
import home.urls
import auth.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jaeweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', RedirectView.as_view(url='/home/')),
    #url(r'^login/$', 'accounts.auth_login.login.auth_login'),
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', RedirectView.as_view(url='/home/')),
    #url(r'^home/$',include(home.urls)),
    #url(r'^overview/$',include(overview.urls)),
    #url(r'^containers/',include(containers.urls)),
    #url(r'^images/',include(images.urls)),
    #url(r'^codeversion/',include(codeversion.urls)),
    url(r'^$', RedirectView.as_view(url='/projects/')),
    url(r'^login/', include(auth.urls)),
    url(r'^projects/$',include(home.urls)),
)
