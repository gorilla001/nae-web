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
        user_name=request.POST.get('name').strip()
        user_email=request.POST.get('email').strip()
        role_id = request.POST.get('role_id').strip()
        data = {
                'project_id' : project_id, 
                'user_name' : user_name,
                'user_email': user_email,
                'role_id':role_id,
        }
        print data
        url='{}/users'.format(BASE_URL)
        headers={'Content-Type':'application/json'}
        rs = requests.post(url,headers=headers,data=json.dumps(data))
    return HttpResponse(json.dumps(rs.json()))


@require_auth
def delete(request):
    user_id=request.GET['id']
    url = '{}/users/{}'.format(BASE_URL,user_id)
    headers={'Content-Type':'application/json'}
    rs = requests.delete(url,headers=headers)
    print rs.json()
    return HttpResponse(json.dumps(rs.json()))

@require_auth
def refresh(request):
    project_id = request.GET.get('project_id')
    url='{}/projects/{}'.format(BASE_URL,project_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    project_info = rs.json() 

    user_id = request.session.get('user_id',None)
    url='{}/users/{}?project_id={}'.format(BASE_URL,user_id,project_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    user_info = rs.json() 
    role=''
    if user_info:
        if user_info['RoleID'] == 1:
    	    role='admin'

    #role = 'normal'
    #if request.session.get('user_id',None) == project_info['admin']:
    #    role = 'admin'

    url='{}/users?project_id={}'.format(BASE_URL,project_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    user_list=rs.json()
    return render_to_response('member-table-replace.html',{'user_list':user_list,'role':role})


    
@require_auth
def admin(request):
    return render_to_response('projects/admin.html')

