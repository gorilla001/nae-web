from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from auth.decorators import require_auth
import requests
import json
from django.http import HttpResponseRedirect
from django.template  import RequestContext
import os
from jaeweb.settings import BASE_URL
import logging


LOG=logging.getLogger('django')

@require_auth
def home(request):
    """get all project list  or projects that belong to specified user."""
    if request.session.get('user_role',None) == 'admin':
        url='{}/projects'.format(BASE_URL)
        headers={'Content-Type':'application/json'}
        rs = requests.get(url,headers=headers)
        projects_list=rs.json()
    else:
        user_id = request.session.get('user_id')
        url='%s/users/%s' % (BASE_URL,user_id)
        headers={'Content-Type':'application/json'}
        rs = requests.get(url,headers=headers)
        projects_list=rs.json()['projects']

    auth_username=request.session.get('user_name')

    return render_to_response('projects.html',{'projects_list':projects_list,'auth_username':auth_username},context_instance=RequestContext(request))

@require_auth
def index(request):
    """show all projects for admin and projects for specified user."""
    if request.session.get('user_role',None) == 'admin':
        url='{}/projects'.format(BASE_URL)
        headers={'Content-Type':'application/json'}
        rs = requests.get(url,headers=headers)
        projects_list=rs.json()
    else:
        user_id = request.session.get('user_id')
        url='%s/users/%s' % (BASE_URL,user_id)
        headers={'Content-Type':'application/json'}
        rs = requests.get(url,headers=headers)
        projects_list=rs.json()['projects']

    """get role for this platform"""
    platform_role=request.session.get('user_role',None)

    auth_username=request.session.get('user_name')
    return render_to_response('project-list.html',{'auth_username':auth_username,'platform_role':platform_role,'projects_list':projects_list},context_instance=RequestContext(request))



@require_auth
def info(request):
    id=request.GET['project_id']
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

    return render_to_response('info-table-replace.html',{'project_info':project_info})

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
    project_id=os.path.basename(request.path)
    project_name = request.GET['name']
    project_desc =  request.GET['desc']
    project_members = request.GET['members']
    project_hgs = request.GET['hgs']
    url='{}/projects/{}?name={}&desc={}&members={}&hgs={}'.format(BASE_URL,project_id,project_name,project_desc,project_members,project_hgs)
    headers={'Content-Type':'application/json'}
    rs = requests.put(url,headers=headers)
    return  HttpResponse(json.dumps(rs.json()))


@require_auth
def detail(request):
    """get project detail by project_id"""
    id=request.GET['id']
    url='{}/projects/{}'.format(BASE_URL,id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    project_info = rs.json() 

    """get user_id from session."""
    user_id = request.session.get('user_id',None)

    """get current user role in project"""
    role = 'default'
    if project_info:
        for user in project_info['users']:
	    if user['name'] == user_id:
                if user['role_id'] == 0:
                    role = 'admin' 

    """get project admin."""
    users = project_info.pop('users')
    admin=[]
    for user in users:
        if user['role_id'] == 0:
            admin.append(user['name'])
    project_info.update({'admin':' '.join(admin)})

    return render_to_response('project.html',
            {'project_info':project_info,
             #'auth_username':auth_username},
             'role':role,
             'user_id': user_id},
            context_instance=RequestContext(request))

@require_auth
def create(request):
    if request.method == 'POST':
        project_name=request.POST.get('name').strip()
        project_desc=request.POST.get('desc').strip()
        project_admin=request.POST.get('admin').strip()
        admin_email = request.POST.get('email').strip()
        base_image = request.POST.get('image').strip()
        data = {
                'name' : project_name, 
                'desc' : project_desc,
                'admin':project_admin,
                'email':admin_email,
		'base_image':base_image,
        }
        url='{}/projects'.format(BASE_URL)
        headers={'Content-Type':'application/json'}
        rs = requests.post(url,headers=headers,data=json.dumps(data))
    return HttpResponse(json.dumps(rs.json()))


@require_auth
def delete(request):
    project_id=request.GET['id']
    url = '{}/projects/{}'.format(BASE_URL,project_id)
    headers={'Content-Type':'application/json'}
    rs = requests.delete(url,headers=headers)
    #return HttpResponseRedirect('/admin/files')
    return HttpResponse("succeed")

    
@require_auth
def admin(request):
    return render_to_response('projects/admin.html')

