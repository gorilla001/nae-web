# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib import auth 

def logout(request):
    #request.session.flush()
    auth.logout(request)
    return HttpResponseRedirect('/')
