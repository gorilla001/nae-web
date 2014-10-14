from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
import requests
import utils
from django.shortcuts import HttpResponseRedirect
from django.template  import RequestContext
from forms import CreateImageForm
import json
from auth.decorators import require_auth
import os
from django.template.loader import render_to_string

# Create your views here.
@require_auth
def index(request):
    project_id = request.GET.get('project_id')
    url='http://localhost:8383/v1/images?project_id=%s' % project_id
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    image_list=rs.json()

    print image_list
    return HttpResponse(json.dumps(image_list))

@require_auth
def show(request):
    image_id=request.GET['id']
    url='http://localhost:8383/v1/images/%s' % image_id
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    print rs.json()
    image_info=rs.json()
    return render_to_response('image_info.html',{'image_info':image_info})


@require_auth
def create(request):
    if request.method == "POST":
        form = CreateImageForm(request.POST)
        if form.is_valid():
            cleaned_data=form.cleaned_data
            project_id=cleaned_data.get('project_id')
            repo_path=cleaned_data.get('repo_path')
            image_desc=cleaned_data.get('image_desc')
            user_name=request.session.get('user_id')
            #image_name=os.path.basename(repo_path)
            image_name=utils.random_str()
            print image_name,project_id,repo_path,image_desc,user_name
            url="http://localhost:8383/v1/images"
            headers={'Content-Type':'application/json'}
            data  = {
                    'image_name':image_name,
                    'project_id':project_id,
                    'repo_path':repo_path,
                    'image_desc':image_desc,
                    'user_name':user_name,
            }
            rs = requests.post(url,headers=headers,data=json.dumps(data))
            print rs.json()
        else:
            print 'form is invalid'
        return HttpResponse(json.dumps(rs.json()))  

@require_auth
def delete(request):
    image_id=request.GET['id']
    f_id=request.GET['f']
    url = 'http://localhost:8383/v1/images/%s?force=%s' % (image_id,f_id)
    headers={'Content-Type':'application/json'}
    rs = requests.delete(url,headers=headers)
    print image_id 
    print rs.json()
    #return HttpResponseRedirect('/admin/files')
    return HttpResponse("succeed")

def update(request):
    project_id = request.GET.get('project_id')
    url='http://localhost:8383/v1/images?project_id=%s' % project_id
    print url
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    print rs.text
    image_list=rs.json()
    print image_list
    return render_to_response('image-table-replace.html',{'image_list':image_list})

