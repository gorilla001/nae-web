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
        url='{}/projects?user_id={}'.format(BASE_URL,user_id)
    print url
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    projects_list=rs.json()
    auth_username=request.session.get('user_name')
    return render_to_response('projects.html',{'projects_list':projects_list,'auth_username':auth_username},context_instance=RequestContext(request))

@require_auth
def index(request):
    if request.session.get('user_role',None) == 'admin':
        url='{}/projects?user_id=admin'.format(BASE_URL)
    else:
        user_id = request.session.get('user_id')
        url='{}/projects?user_id={}'.format(BASE_URL,user_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    projects_list=rs.json()
    role=request.session.get('user_role',None)
    auth_username=request.session.get('user_name')
    return render_to_response('project-list.html',{'auth_username':auth_username,'role':role,'projects_list':projects_list},context_instance=RequestContext(request))



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
    users = project_info.pop('users')
    admin=[]
    for user in users:
        if user['role_id'] == 0:
            admin.append(user['name'])
    project_info.update({'admin':' '.join(admin)})

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
        user_name=request.POST.get('name').strip()
        user_email=request.POST.get('email').strip()
        role_id = request.POST.get('role_id').strip()
        data = {
                'project_id' : project_id, 
                'name' : user_name,
                'email': user_email,
                'role_id':role_id,
        }
        print data
        url='{}/users'.format(BASE_URL)
        headers={'Content-Type':'application/json'}
        requests.post(url,headers=headers,data=json.dumps(data))
    return HttpResponse("")


@require_auth
def delete(request):
    user_id=request.GET['id']
    url = '{}/users/{}'.format(BASE_URL,user_id)
    headers={'Content-Type':'application/json'}
    requests.delete(url,headers=headers)
    return HttpResponse("") 

@require_auth
def refresh(request):
    """get all users for project_id."""
    project_id = request.GET.get('project_id')
    url='{}/projects/{}'.format(BASE_URL,project_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    project_info = rs.json() 
    user_list = project_info['users']

    """get project role for current user."""
    user_id = request.session.get('user_id',None)
    project_role=None
    for user in user_list:
        if user['name'] == user_id:
    	    project_role = user['role_id']
	 
    """check if current user is superuser"""
    if request.session.get('user_role',None) == 'admin':
       role = 0    
    elif project_role == 0:
       role = 0
    else:
       role = project_role

    # Sorted user lists by role_id
    user_list = sorted(user_list,key = lambda x:x['role_id'])

    return render_to_response('member-table-replace.html',{'user_list':user_list,'role':role})


    
@require_auth
def admin(request):
    return render_to_response('projects/admin.html')

