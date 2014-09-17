from django.shortcuts import render
from django.http import HttpResponse
from django.template  import RequestContext
from django.shortcuts import render_to_response
# Create your views here.
from auth.decorators import require_auth
from models import Projects
from models import DockerFiles 
import utils
from django.shortcuts import HttpResponseRedirect

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
    file_list=DockerFiles.objects.all()
    return render_to_response('admin/files.html',{'file_list':file_list},context_instance=RequestContext(request))

@require_auth
def createFile(request):
    if request.method == 'POST':
        print request.POST.get("filename","test")
        print request.POST.get("content","")
        file_name=request.POST.get("filename","test")
        dockerfile=utils.create_file(file_name)
        utils.write_file(dockerfile,request.POST.get("content",""))

        file_path=utils.get_file_path(file_name)
        file_size=utils.get_file_size(file_path)
        created=utils.get_current_datatime()
        created_by=request.session.get("auth_username")
        modified=created
        modified_by=created_by 
        path=file_path
        data=DockerFiles(Name=file_name,Size=file_size,Created=created,CreatedBy=created_by,Modified=modified,ModifiedBy=modified_by,Path=path)
        data.save()
    return HttpResponseRedirect('/admin/files')

@require_auth
def showFile(request):
    filepath=request.GET['filepath']
    with open(filepath,"r") as f:
        data=f.read()
    return HttpResponse(data)


@require_auth
def users(request):
    print 'users'
    return render_to_response('admin/users.html')
