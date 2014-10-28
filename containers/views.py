from django.http import HttpResponse
from django.shortcuts import render_to_response
import requests
from auth.decorators import require_auth
from django.http import HttpResponseRedirect
import json
from jaeweb.settings import BASE_URL

# Create your views here.

@require_auth
def index(request):
    #container_list = Containers.objects.all() 
    #print container_list
    project_id = request.GET.get('project_id')
    user_id = request.GET.get('user_id')
    url="{}/containers?project_id={}&user_id={}".format(BASE_URL,project_id,user_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    container_list = rs.json()
    print container_list
    return render_to_response('container-table-replace.html',{'container_list':container_list})

@require_auth
def detail(request):
    #project_id=os.path.basename(request.path)
    container_id=request.GET['id']
    print container_id
    url='{}/containers/{}'.format(BASE_URL,container_id)
    headers={'Content-Type':'application/json'}
    print url,headers
    rs = requests.get(url,headers=headers)
    container_info = rs.json()
    return render_to_response('container_info.html',{'container_info':container_info})


@require_auth
def create(request):
    if request.method == 'POST':
        container_environ = request.POST.get('container_env') 
        container_project = request.POST.get('project_id')
        container_image = request.POST.get('image_name')
        container_hg = request.POST.get('container_hg')
        container_code = request.POST.get('container_code')
        app_type = request.POST.get('app_type')
        user_name = request.session.get('user_id')
        user_key = request.session.get('user_key')

        print container_environ,container_project,container_hg,container_code
        url='{}/containers'.format(BASE_URL)
        headers={'Content-Type':'application/json'}
        data = {
                'container_environ':container_environ,
                'container_project':container_project,
                'container_image':container_image,
                'container_hg':container_hg,
                'container_code':container_code,
                'app_type':app_type,
                'user_name':user_name,
                'user_key':user_key,
        }
        print json.dumps(data)
        rs = requests.post(url,headers=headers,data=json.dumps(data))
        print rs.json()
    return HttpResponseRedirect('/containers')

@require_auth
def delete(request):
    container_id=request.GET['id']
    v=request.GET['v']
    url = '{}/containers/{}?v={}'.format(BASE_URL,container_id,v)
    headers={'Content-Type':'application/json'}
    requests.delete(url,headers=headers)
    return HttpResponse("succeed")

@require_auth
def update(request):
    project_id = request.GET.get('project_id')
    user_id = request.GET.get('user_id')
    url='{}/containers?project_id={}&user_id={}'.format(BASE_URL,project_id,user_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    container_list = rs.json()
    return render_to_response('container-table-replace.html',{'container_list':container_list})

@require_auth
def stop(request):
    ctn_id = request.GET['id']
    url = '{}/containers/{}/stop'.format(BASE_URL,ctn_id)
    headers={'Content-Type':'application/json'}
    requests.post(url,headers=headers)
    return HttpResponse("succeed")
