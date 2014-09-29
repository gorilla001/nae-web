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
    #image_list=[]
    #result=requests.get('http://localhost:8383/v1/images')
    #result_dict=result.json()
    #for res in result_dict:
    #    _dict={}
    #    _dict['Container_Id']=res['Id'][:12]
    #    _dict['Name']=res['RepoTags'][0]
    #    _dict['VirtualSize']=utils.byte_to_gb(res['VirtualSize'])
    #    _dict['Created']=utils.timestamp_to_local(res['Created'])
    #    _dict['Environ']='develop'
    #    image_list.append(_dict)
    #return render_to_response('images.html',data=image_list)
    url='http://localhost:8383/v1/projects'
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    projects_list=rs.json()

    url='http://localhost:8383/v1/images'
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    images_list=rs.json()

    auth_username=request.session.get('realname')
    role=request.session.get('role',None)
    return render_to_response('images.html',
                            {'auth_username':auth_username,
                             'role':role,
                             'projects_list':projects_list,
                             'images_list':images_list,
                             },
                             context_instance=RequestContext(request)
                            )
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
            #image_name=cleaned_data.get('image_name',utils.random_str())
            image_proj=cleaned_data.get('image_proj')
            repo_path=cleaned_data.get('repo_path')
            image_desc=cleaned_data.get('image_desc')
            user_name=request.session.get('nickname')
            image_name=os.path.basename(repo_path)
            print image_name,image_proj,repo_path,image_desc,user_name
            url="http://localhost:8383/v1/images"
            headers={'Content-Type':'application/json'}
            data  = {
                    'image_name':image_name,
                    'image_proj':image_proj,
                    'repo_path':repo_path,
                    'image_desc':image_desc,
                    'user_name':user_name,
            }
            rs = requests.post(url,headers=headers,data=json.dumps(data))
            print rs.json()
        else:
            print 'form is invalid'
    return HttpResponseRedirect('/images')

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
    url='http://localhost:8383/v1/images'
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    print rs.text
    images_list=rs.json()
    #return render_to_response(
    #        'images_content.html',
    #        {'images_list':images_list}
    #        )
    return render_to_response('images_content.html',{'images_list':images_list})

