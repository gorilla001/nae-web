from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from containers.models import Containers
import requests
from auth.decorators import require_auth
from django.http import HttpResponseRedirect
from django.template  import RequestContext
import json
from pprint import pprint

# Create your views here.

@require_auth
def index(request):
    #container_list = Containers.objects.all() 
    #print container_list
    auth_username = request.session.get('realname')
    role = request.session.get('role')

    url="http://localhost:8383/v1/containers"
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    containers_list=rs.json()
    pprint(containers_list)

    url="http://localhost:8383/v1/projects"
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    projects_list = rs.json() 
    print rs.json()
    images_list=[]
    total_containers = len(containers_list) 
    print 'total_containers',total_containers
    return render_to_response('containers.html',
                            {'auth_username':auth_username,
                             'role':role,
                             'containers_list':containers_list,
                             'projects_list':projects_list,
                             'image_list':images_list
                             },
                            context_instance=RequestContext(request))
@require_auth
def detail(request):
    #project_id=os.path.basename(request.path)
    container_id=request.GET['id']
    print container_id
    url='http://localhost:8383/v1/containers/%s' % container_id
    headers={'Content-Type':'application/json'}
    print url,headers
    rs = requests.get(url,headers=headers)
    container_info = rs.json()
    return render_to_response('container_info.html',{'container_info':container_info})


@require_auth
def create(request):
    if request.method == 'POST':
        container_environ = request.POST.get('container_environ') 
        container_project = request.POST.get('container_project')
        #container_image = request.POST.get('container_image')
        container_hgs = request.POST.get('container_image')
        container_code = request.POST.get('container_code')
        user_name = request.session.get('nickname')

        print container_environ,container_project,container_hgs,container_code
        url='http://localhost:8383/v1/containers'
        headers={'Content-Type':'application/json'}
        data = {
                'container_environ':container_environ,
                'container_project':container_project,
                'container_image':container_hgs,
                'container_code':container_code,
                'user_name':user_name,
        }
        print json.dumps(data)
        rs = requests.post(url,headers=headers,data=json.dumps(data))
        print rs.json()
        #project_name=request.POST.get('name').strip()
        #project_hgs=request.POST.get('hgaddrs').splitlines()
        #project_members=request.POST.get('members').splitlines()
        #project_desc=request.POST.get('desc').strip()
        #project_admin=request.session['nickname']
        #print request.POST.get('members')
        #print project_members
        #data = {
        #        'project_name' : project_name, 
        #        'project_hgs' :  project_hgs, 
        #        'project_members' : project_members,
        #        'project_desc' : project_desc,
        #        'project_admin':project_admin,
        #}
        #print data
        #url='http://localhost:8383/v1/projects'
        #headers={'Content-Type':'application/json'}
        #rs = requests.post(url,headers=headers,data=json.dumps(data))
        #print rs.json()
    return HttpResponseRedirect('/containers')

@require_auth
def delete(request):
    container_id=request.GET['id']
    url = 'http://localhost:8383/v1/containers/{}'.format(container_id)
    headers={'Content-Type':'application/json'}
    rs = requests.delete(url,headers=headers)
    print 'here'
    print rs.json()
    #return HttpResponseRedirect('/admin/files')
    return HttpResponse("succeed")
