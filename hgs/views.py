from django.http import HttpResponse
from django.shortcuts import render_to_response
from auth.decorators import require_auth
# Create your views here.
import requests
import json
from django.template  import RequestContext
import os
from jaeweb.settings import BASE_URL

@require_auth
def home(request):
    if request.session.get('user_role',None) == 'admin':
        url='{}/projects?user_id=admin'.format(BASE_URL)
    else:
        user_id = request.session.get('user_id')
        url='http://localhost:8383/v1/projects?user_id={}'.format(user_id)
    print url
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    projects_list=rs.json()
    auth_username=request.session.get('user_name')
    return render_to_response('projects.html',{'projects_list':projects_list,'auth_username':auth_username},context_instance=RequestContext(request))

@require_auth
def index(request):
    project_id = request.GET.get('project_id')
    url='{}/repos?project_id={}'.format(BASE_URL,project_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    hg_list=rs.json()

    return HttpResponse(json.dumps(hg_list)) 



@require_auth
def info(request):
    name=request.GET['name']
    url='{}/projects/{}'.format(BASE_URL,name)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    project_info = rs.json()

    users_list = []
    return render_to_response('project.html',{'project_info':project_info,'users_list':users_list})

@require_auth
def list(request):
    url='{}/projects'.format(BASE_URL)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    projects_list=rs.json()
    role=request.session.get('user_role',None)
    auth_username=request.session.get('realname')
    return render_to_response('project-list.html',{'projects_list':projects_list,'auth_username':auth_username,'role':role},context_instance=RequestContext(request))

@require_auth
def show(request):
    project_id=os.path.basename(request.path)
    url='{}/projects/{}'.format(BASE_URL,project_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    print rs.json()
    return  HttpResponse(json.dumps(rs.json()))
@require_auth
def update(request):

    project_id=request.GET.get('project_id')
    url='{}/users?project_id={}'.format(BASE_URL,project_id)
    headers={'Content-Type':'application/json'}
    rs = requests.put(url,headers=headers)
    print rs.json()
    return  HttpResponse(json.dumps(rs.json()))


@require_auth
def detail(request):
    id=request.GET['id']
    url='{}/projects/{}'.format(BASE_URL,id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    project_info = rs.json() 
    role = ''
    if request.session.get('user_id',None) == project_info['admin']:
        role = 'admin'

    auth_username=request.session.get('user_name')
    url='{}/users?project_id={}'.format(BASE_URL,id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    user_list = rs.json() 

    url='{}/images?project_id={}'.format(BASE_URL,id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    image_list = rs.json() 

    print user_list

    return render_to_response('project.html',
            {'project_info':project_info,
             'user_list':user_list,
             'image_list':image_list,
             'auth_username':auth_username,
             'role':role},
            context_instance=RequestContext(request))




@require_auth
def create(request):
    if request.method == 'POST':
        project_id=request.POST.get('project_id').strip()
        repo_path = request.POST.get('hg_addr').strip()
        data = {
                'project_id' : project_id, 
                'repo_path':repo_path,
        }
        url='{}/repos'.format(BASE_URL)
        headers={'Content-Type':'application/json'}
        requests.post(url,headers=headers,data=json.dumps(data))
    return HttpResponse({"status":200})


@require_auth
def delete(request):
    hg_id=request.GET['id']
    url = '{}/repos/{}'.format(BASE_URL,hg_id)
    headers={'Content-Type':'application/json'}
    rs = requests.delete(url,headers=headers)
    return HttpResponse(json.dumps(rs.json()))

@require_auth
def refresh(request):
    """get repos list from project_id"""
    project_id = request.GET.get('project_id')
    url = '%s/repos?project_id=%s' % (BASE_URL,project_id)  
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    hg_list = rs.json()
    
    """get current user id."""
    user_id = request.session.get('user_id',None)

    """get current user role in current project."""
    url='%s/projects/%s' % (BASE_URL,project_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    users = rs.json()['users'] 
    """if current user not in project,project role will be None."""
    project_role = None
    """if current user is in project,project role will be override."""
    for user in users:
        if user['name'] == user_id:
            project_role = user['role_id']
    return render_to_response('hg-table-replace.html',{'hg_list':hg_list,'project_role':project_role})


    
@require_auth
def admin(request):
    return render_to_response('projects/admin.html')

