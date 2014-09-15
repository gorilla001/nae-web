from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
# Create your views here.
from auth.decorators import require_auth
from models import Projects

@require_auth
def index(request):
    print 'index'
    return render_to_response('admin/home.html')

@require_auth
def projects(request):
    projects_list=Projects.objects.all()
    return render_to_response('admin/projects.html',projects_list)

@require_auth
def images(request):
    print 'images'
    return render_to_response('admin/images.html')


@require_auth
def files(request):
    print 'files'
    return render_to_response('admin/files.html')
@require_auth
def users(request):
    print 'users'
    return render_to_response('admin/users.html')
