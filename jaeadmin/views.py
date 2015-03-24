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
import requests
import json
from jaeweb.settings import DOCKER_ENDPOINT 

#@require_auth
def index(request):
    return render_to_response('admin/overview.html')

@require_auth
def projects(request):
    #url='http://localhost:8383/v1/projects'
    #headers={'Content-Type':'application/json'}
    #rs = requests.get(url,headers=headers)
    #projects_list=rs.json()
    #print projects_list

    #url='http://localhost:8383/v1/images'
    #headers={'Content-Type':'application/json'}
    #rs = requests.get(url,headers=headers)
    #image_list = rs.json()

    #url='http://localhost:8383/v1'
    #headers={'Content-Type':'application/json'}
    #r=requests.get("{}/users".format(url),headers=headers)
    #user_list=r.json()

    #return render_to_response('admin/projects.html',{'projects_list':projects_list,'image_list':image_list,'user_list':user_list},context_instance=RequestContext(request))
    return render_to_response('admin/projects.html',context_instance=RequestContext(request))

def createProject(request):
    if request.method == 'POST':
        data = {
                'project_name' : request.POST.get('name'),
                'project_image' : request.POST.get('image'),
                'project_admin':request.POST.get('admin'),
                'project_desc':request.POST.get('desc'),
                'created_by':request.session['auth_username'],
        }
        url='http://localhost:8383/v1/projects'
        headers={'Content-Type':'application/json'}
        rs = requests.post(url,headers=headers,data=json.dumps(data))
        print rs.json()
    return HttpResponseRedirect('/admin/projects')

@require_auth
def images(request):
    url = "%s/images/json" % DOCKER_ENDPOINT
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    images_list=rs.json()
    return render_to_response('admin/images.html',{'images_list':images_list},context_instance=RequestContext(request))

@require_auth
def createImage(request):
    if request.method == 'POST':
        image_name=request.POST.get('imagename')
        image_desc=request.POST.get('description')
        docker_file=request.POST.get('dockerfile')
        user_name=request.session['auth_username']

        repo_path=utils.get_repo_path(docker_file)
        url='http://localhost:8383/v1/images'
        data={
                'image_name':image_name,
                'image_desc':image_desc,
                'repo_path': repo_path,
                'user_name':user_name,
         }
        headers={'Content-Type':'applicaton/json'}
        rs=requests.post(url,data=json.dumps(data),headers=headers)
        print rs.json()
    return HttpResponseRedirect('/admin/images')


@require_auth
def containers(request):
    url = "%s/containers/json?all=1" % DOCKER_ENDPOINT
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    containers_list=rs.json()
    for container in containers_list:
        uuid = container['Id']
    return render_to_response('admin/containers.html',{'containers_list': containers_list},context_instance=RequestContext(request))

@require_auth
def registries(request):
    return render_to_response('admin/registries.html',context_instance=RequestContext(request))

@require_auth
def hosts(request):
    return render_to_response('admin/hosts.html',context_instance=RequestContext(request))

@require_auth
def regions(request):
    return render_to_response('admin/regions.html',context_instance=RequestContext(request))

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
        file_name=request.POST.get("filename","test")
        #save file to localhost repo
        repo_path=utils.get_repo_path(file_name)
        rev_control=utils.MercurialRevisionControl()
        rev_control.create_repo(repo_path)

        auth_user=request.session['auth_username']
        rev_control.hg_rc(repo_path,'ui','username',auth_user)

        file_content=request.POST.get("content","")
        utils.create_file(repo_path,file_content)

        rev_control.add(repo_path)
        rev_control.commit(repo_path)
        #utils.write_file(dockerfile,request.POST.get("content",""))
        #revision_control=utils.MercurialRevisionControl()
        #revision_control.create_repo(
        #save file to db
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
    url='http://localhost:8383/v1'
    headers={'Content-Type':'application/json'}
    r=requests.get("{}/users".format(url),headers=headers)
    user_list=r.json()
    return render_to_response('admin/users.html',{'user_list':user_list},context_instance=RequestContext(request))
def createUser(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')  
        cn_name = request.POST.get('cnname')
        department = request.POST.get('department')
        email = request.POST.get('email')

        print user_name,cn_name,department,email
        url = 'http://localhost:8383/v1/users'
        data = {
                'user_name':user_name,
                'cn_name':cn_name,
                'department':department,
                'email':email,
        }
        headers={'Content-Type':'application/json'}
        r=requests.post("{}".format(url),headers=headers,data=json.dumps(data))
        print 'create user:',r.json()
    return HttpResponseRedirect('/admin/users')
