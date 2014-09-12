from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
# Create your views here.
from auth.decorators import require_auth
from django.contrib.auth.decorators import login_required

@require_auth
def index(request):
    return render_to_response('home.html')
