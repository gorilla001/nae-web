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
from jaeweb.settings import BASE_URL

#@require_auth
def index(request):
    url = "%s/images/json" % DOCKER_ENDPOINT
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    images_list=rs.json()

    url = "%s/containers/json?all=1" % DOCKER_ENDPOINT
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    containers_list=rs.json()
   
    running=0
    for container in containers_list:
        status = container['Status']
        if 'Up' in status:
            running += 1

    stopped = len(containers_list) - running


    url = "%s/projects" % BASE_URL
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    projects_list = rs.json() 
    return render_to_response('admin/overview.html',
                             {'image':len(images_list),
                              'container':len(containers_list),
                              'project': len(projects_list),
                              'running':running,
                              'stopped':stopped})

@require_auth
def projects(request):
    url='%s/projects' % BASE_URL
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    projects_list=rs.json()

    return render_to_response('admin/projects.html',
                             {'projects_list': projects_list},
                             context_instance=RequestContext(request))

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
    images_list_all=rs.json()

    url="%s/images" % BASE_URL
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    images_list_db=rs.json()

    images_list = []
    for image in images_list_all:
        for _image in images_list_db:
            if _image['uuid'] == image['Id']:
                project_id = _image['project_id']
                url = "%s/projects/%s" % (BASE_URL,project_id)
                resp = requests.get(url)
                project_name = resp.json().get('name')
                _ = {'ProjectName': project_name}
                image.update(_)
        images_list.append(image)
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
    containers_list_all=rs.json()

    url="%s/containers" % BASE_URL
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    containers_list_db=rs.json()
    
    containers_list = []
    for container in containers_list_all:
        for _container in containers_list_db:
            if _container['uuid'] == container['Id']:
                project_id = _container['project_id']
                url = "%s/projects/%s" % (BASE_URL,project_id)
                resp = requests.get(url)
                project_name = resp.json().get('name')
                _ = {'ProjectName': project_name,'UserId':_container['user_id']}
                container.update(_)
               
                host_id = _container['host_id'] 
                url = "%s/hosts/%s" % (BASE_URL,host_id) 
                resp = requests.get(url)
                host_ip = resp.json().get('host')
                zone = resp.json().get('zone')
                _ = {'Host': host_ip,'Zone': zone} 
                container.update(_)

        containers_list.append(container)
    return render_to_response('admin/containers.html',{'containers_list': containers_list},context_instance=RequestContext(request))

@require_auth
def registries(request):
    return render_to_response('admin/registries.html',context_instance=RequestContext(request))

@require_auth
def hosts(request):
    url = "%s/hosts" % BASE_URL
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    hosts_list=rs.json()
   
    return render_to_response('admin/hosts.html',{'hosts_list': hosts_list}, context_instance=RequestContext(request))

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

@require_auth
def events(request):
    return render_to_response('admin/events.html')
