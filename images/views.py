from django.http import HttpResponse
from django.shortcuts import render_to_response
import requests
from forms import CreateImageForm
import json
from auth.decorators import require_auth
from jaeweb.settings import BASE_URL
import os
import logging

logger=logging.getLogger(__name__)

# Create your views here.
@require_auth
def index(request):
    project_id = request.GET.get('project_id')
    url='{}/images?project_id={}'.format(BASE_URL,project_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    image_list=rs.json()

    return HttpResponse(json.dumps(image_list))

@require_auth
def show(request):
    image_id=request.GET['id']
    url='{}/images/{}'.format(BASE_URL,image_id)
    headers={'Content-Type':'application/json'}
    resp = requests.get(url,headers=headers)
    print resp.json()
    return HttpResponse(json.dumps(resp.json())) 


@require_auth
def create(request):
    if request.method == "POST":
        form = CreateImageForm(request.POST)
        if form.is_valid():
            cleaned_data=form.cleaned_data
            project_id=cleaned_data.get('project_id')
            repos_id=cleaned_data.get('repos_id')

            url="%s/repos/%s" % (BASE_URL, repos_id)
            headers={'Content-Type':'application/json'}
            rs = requests.get(url,headers=headers)
            repo_path = rs.json().get("repo_path")

            repo_branch=cleaned_data.get('repo_branch')
            image_desc=cleaned_data.get('image_desc')
            user_name=request.session.get('user_id')
            #image_name=os.path.basename(repo_path)
            image_name= os.path.basename(repo_path) + '-' + repo_branch
            url="{}/images".format(BASE_URL)
            headers={'Content-Type':'application/json'}
            data  = {
                    'name':image_name,
                    'project_id':project_id,
                    'repos_id':repos_id,
                    'branch':repo_branch,
                    'desc':image_desc,
                    'user_id':user_name,
            }
            print data
            rs = requests.post(url,headers=headers,data=json.dumps(data))
            logger.debug(rs.json())
        else:
            logger.debug('form is invalid')
        return HttpResponse(json.dumps(rs.json()))  

@require_auth
def delete(request):
    image_id=request.GET['id']
    f_id=request.GET['f']
    url = '{}/images/{}?force={}'.format(BASE_URL,image_id,f_id)
    headers={'Content-Type':'application/json'}
    rs = requests.delete(url,headers=headers)
    return HttpResponse(json.dumps(rs.json()))

@require_auth
def update(request):
    """get images list by project id."""
    project_id = request.GET.get('project_id')
    url='{}/images?project_id={}'.format(BASE_URL,project_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    image_list=rs.json()

    """get current user id."""
    user_id = request.session.get('user_id',None)

    """get current user role in current project."""
    url='%s/projects/%s' % (BASE_URL,project_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    users = rs.json()['users'] 
    project_role=None
    for user in users:
        if user['name'] == user_id:
            project_role = user['role_id']
    if request.session.get('user_role',None) == 'admin':
        role=0
    elif project_role == 0:
        role=0
    else:
        role=project_role

    return render_to_response('image-table-replace.html',{'image_list':image_list,'role':role})

@require_auth
def edit(request):
    img_id = request.GET['id']
    url = '%s/images/%s/edit' % (BASE_URL,img_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    return HttpResponse(json.dumps(rs.json()))

@require_auth
def commit(request):
    repo=request.GET.get('repo')
    tag=request.GET.get('tag')
    ctn=request.GET.get('ctn')
    id=request.GET.get('id')
    proj_id = request.GET.get('proj_id') 
    url="{}/images/commit?repo={}&tag={}&ctn={}&id={}&proj_id={}".format(BASE_URL,repo,tag,ctn,id,proj_id)
    headers={'Content-Type':'application/json'}
    rs = requests.post(url,headers=headers)
    return HttpResponse(json.dumps(rs.json()))

@require_auth
def conflict(request):
    id=request.GET.get('id')
    url="{}/images/conflict/{}".format(BASE_URL,id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    container_list = rs.json()
    return render_to_response('image-conflict-table.html',{'container_list':container_list})

@require_auth
def base(request):
    url="{}/baseimages".format(BASE_URL,id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    image_list = rs.json()
    return HttpResponse(json.dumps(image_list))

@require_auth
def destroy(request):
    name = request.GET.get('name')
    url="%s/images/%s/destroy" % (BASE_URL,name)
    headers={'Content-Type':'application/json'}
    rs = requests.post(url,headers=headers)
    return HttpResponse(json.dumps(rs.json()))
    


    
	
