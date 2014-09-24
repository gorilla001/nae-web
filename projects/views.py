from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from auth.decorators import require_auth
# Create your views here.
import requests
import json
from django.http import HttpResponseRedirect
from django.template  import RequestContext
import os

@require_auth
def index(request):
    url='http://localhost:8383/v1/projects'
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    projects_list=rs.json()
    role=request.session.get('role',None)
    auth_username=request.session.get('auth_username','test')
    return render_to_response('projects.html',{'projects_list':projects_list,'auth_username':auth_username,'role':role},context_instance=RequestContext(request))

@require_auth
def show(request):
    project_id=os.path.basename(request.path)
    url='http://localhost:8383/v1/projects/%s' % project_id
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    print rs.json()
    return HttpResponse(json.dumps(rs.json()))

@require_auth
def create(request):
    if request.method == 'POST':
        project_name=request.POST.get('name').strip()
        project_hgs=request.POST.get('hgaddrs').splitlines()
        project_members=request.POST.get('members').splitlines()
        project_desc=request.POST.get('desc').strip()
        project_admin=request.session['auth_username']
        data = {
                'project_name' : project_name, 
                'project_hgs' :  project_hgs, 
                'project_members' : project_members,
                'project_desc' : project_desc,
                'project_admin':project_admin,
        }
        url='http://localhost:8383/v1/projects'
        headers={'Content-Type':'application/json'}
        rs = requests.post(url,headers=headers,data=json.dumps(data))
        print rs.json()
    return HttpResponseRedirect('/projects')


@require_auth
def delete(request):
    project_id=request.GET['id']
    url = 'http://localhost:8383/v1/projects/%s' % project_id
    headers={'Content-Type':'application/json'}
    rs = requests.delete(url,headers=headers)
    print project_id 
    print rs.json()
    #return HttpResponseRedirect('/admin/files')
    return HttpResponse("succeed")

    
@require_auth
def admin(request):
    return render_to_response('projects/admin.html')

