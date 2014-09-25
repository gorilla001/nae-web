from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from auth.decorators import require_auth

# Create your views here.
@require_auth
def index(request):
    #return HttpResponse("Hello,World")
    auth_username = request.session.get('realname')
    return render_to_response('overview.html',{'auth_username':auth_username})
