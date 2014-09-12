import functools
from django.utils.decorators import available_attrs
from django.http import HttpResponseRedirect
from jaeweb.settings import LOGIN_URL
from django.contrib.auth.models import User

def require_auth(view_func):

    @functools.wraps(view_func, assigned=available_attrs(view_func))
    def dec(request, *args, **kwargs):
        if request.session.get('auth_username', None): 
            return view_func(request, *args, **kwargs)
        return HttpResponseRedirect(LOGIN_URL)
    return dec

