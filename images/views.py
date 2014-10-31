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

    print image_list
    return HttpResponse(json.dumps(image_list))

@require_auth
def show(request):
    image_id=request.GET['id']
    url='{}/images/{}'.format(BASE_URL,image_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    print rs.json()
    return HttpResponse(json.dumps(rs.json())) 


@require_auth
def create(request):
    if request.method == "POST":
        form = CreateImageForm(request.POST)
        if form.is_valid():
            cleaned_data=form.cleaned_data
            project_id=cleaned_data.get('project_id')
            repo_path=cleaned_data.get('repo_path')
            repo_branch=cleaned_data.get('repo_branch')
            image_desc=cleaned_data.get('image_desc')
            user_name=request.session.get('user_id')
            #image_name=os.path.basename(repo_path)
            image_name= os.path.basename(repo_path) + '-' + repo_branch
            print image_name,project_id,repo_path,image_desc,user_name
            url="{}/images".format(BASE_URL)
            headers={'Content-Type':'application/json'}
            data  = {
                    'image_name':image_name,
                    'project_id':project_id,
                    'repo_path':repo_path,
                    'repo_branch':repo_branch,
                    'image_desc':image_desc,
                    'user_name':user_name,
            }
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
    print image_id 
    print rs.json()
    return HttpResponse("succeed")

@require_auth
def update(request):
    project_id = request.GET.get('project_id')
    url='{}/images?project_id={}'.format(BASE_URL,project_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    image_list=rs.json()
    logger.debug(image_list)
    return render_to_response('image-table-replace.html',{'image_list':image_list})

@require_auth
def edit(request):
    img_id = request.GET['id']
    url = '{}/images/edit?id={}'.format(BASE_URL,img_id)
    headers={'Content-Type':'application/json'}
    rs = requests.post(url,headers=headers)
    print rs.json()
    return HttpResponse(json.dumps(rs.json()))

@require_auth
def commit(request):
    repo=request.GET.get('repo')
    tag=request.GET.get('tag')
    ctn=request.GET.get('ctn')
    id=request.GET.get('id')
    url="{}/images/commit?repo={}&tag={}&ctn={}&id={}".format(BASE_URL,repo,tag,ctn,id)
    headers={'Content-Type':'application/json'}
    rs = requests.post(url,headers=headers)
    return HttpResponse(json.dumps(rs.json()))
    
	
