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
import os

@require_auth
def index(request):
    print 'index'
    return render_to_response('admin/preview.html')

@require_auth
def projects(request):
    projects_list=Projects.objects.all()
    return render_to_response('admin/projects.html',projects_list)

@require_auth
def images(request):
    print 'images'
    image_list=[]
    file_list = DockerFiles.objects.values('Name')
    return render_to_response('admin/images.html',{'file_list':file_list,'image_list':image_list},context_instance=RequestContext(request))

@require_auth
def createImage(request):
    if request.method == 'POST':
        print request.POST.get('imagename')
        print request.POST.get('description')
        print request.POST.get('dockerfile')
    return HttpResponseRedirect('/admin/images')


@require_auth
def files(request):
    file_list=DockerFiles.objects.all()
    return render_to_response('admin/files.html',{'file_list':file_list},context_instance=RequestContext(request))

@require_auth
def getFiles(request):
    _file_list=DockerFiles.objects.all()
    file_list = _file_list.Name.all()
    return HttpResponse(file_list)
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
def deleteFile(request):
    filepath=request.GET['filepath']
    if os.path.isfile(filepath):
        os.remove(filepath)
    data=DockerFiles.objects.get(Path=filepath)
    data.delete()
    print 'herehere'
    #return HttpResponseRedirect('/admin/files')
    return HttpResponse("succeed")



@require_auth
def users(request):
    print 'users'
    return render_to_response('admin/users.html')
