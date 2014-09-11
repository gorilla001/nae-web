from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from containers.models import Containers

# Create your views here.

def index(request):
    container_list = Containers.objects.all() 
    print container_list
    return render_to_response('containers.html',container_list)
