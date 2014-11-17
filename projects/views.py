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

# Create your views here.

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
    print projects_list
    return render_to_response('project-list.html',{'auth_username':auth_username,'role':role,'projects_list':projects_list},context_instance=RequestContext(request))



@require_auth
def info(request):
    id=request.GET['project_id']
    url='{}/projects/{}'.format(BASE_URL,id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    project_info = rs.json()

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
    print rs.json()
    return  HttpResponse(json.dumps(rs.json()))


@require_auth
def detail(request):
    id=request.GET['id']
    url='{}/projects/{}'.format(BASE_URL,id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    project_info = rs.json() 

    #role = 'normal'
    #if request.session.get('user_id',None) == project_info['admin']:
    #    role = 'admin'
    auth_username=request.session.get('user_name')
    user_id = request.session.get('user_id',None)

    url='{}/users/{}?project_id={}'.format(BASE_URL,user_id,id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    user_info = rs.json() 
    if user_info:
        if user_info['RoleID'] == 1:
    	    role='admin'

    return render_to_response('project.html',
            {'project_info':project_info,
             'auth_username':auth_username,
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
        data = {
                'project_name' : project_name, 
                'project_desc' : project_desc,
                'project_admin':project_admin,
                'admin_email':admin_email,
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
    print project_id 
    print rs.json()
    #return HttpResponseRedirect('/admin/files')
    return HttpResponse("succeed")

    
@require_auth
def admin(request):
    return render_to_response('projects/admin.html')

