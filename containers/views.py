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
    project_id = request.GET.get('project_id')
    user_id = request.GET.get('user_id')
    url="{}/containers?project_id={}&user_id={}".format(BASE_URL,project_id,user_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    container_list_org = rs.json()
    #for container in container_list:
    #    image_id = container.pop('image_id',None)
    #    image = ""
    #    if image_id: 
    #        url='{}/images/{}'.format(BASE_URL,image_id)
    #        headers={'Content-Type':'application/json'}
    #        resp = requests.get(url,headers=headers)
    #        try:
    #            image = "%s:%s" % (resp.json()['name'],resp.json()['tag'])
    #        except KeyError as ex:
    #            raise
    #    container.update({"image":image})
    #    container_list.append(container)
    container_list = []
    for container in container_list_org:
        repos = container.pop("repos",None)
        if repos is not None:
            repos = repos.split("/")[-1] 
        container.update({"repos":repos})
        container_list.append(container)

    """get current user role in current project."""
    url='%s/projects/%s' % (BASE_URL,project_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    users = rs.json()['users'] 
    project_role=None
    for user in users:
        if user['name'] == user_id:
            project_role = user['role_id']
   
    return render_to_response('container-table-replace.html',
                             {'container_list':container_list,
                              'project_role': project_role})

@require_auth
def detail(request):
    #project_id=os.path.basename(request.path)
    container_id=request.GET['id']
    url='{}/containers/{}'.format(BASE_URL,container_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    container_info = rs.json()
    return render_to_response('container_info.html',{'container_info':container_info})


@require_auth
def create(request):
    if request.method == 'POST':
        container_environ = request.POST.get('container_env') 
        container_project = request.POST.get('project_id')
        container_image   = request.POST.get('image_name')
        container_hg      = request.POST.get('container_hg')
        container_code    = request.POST.get('container_code')
        app_type          = request.POST.get('app_type')
        user_name         = request.session.get('user_id')
        user_key          = request.session.get('user_key')
        zone_id           = request.POST.get('zone_id')

        url='{}/containers'.format(BASE_URL)
        headers={'Content-Type':'application/json'}
        data = {
                'env':container_environ,
                'project_id':container_project,
                'image_id':container_image,
                'repos':container_hg,
                'branch':container_code,
                'app_type':app_type,
                'user_id':user_name,
                'user_key':user_key,
                'zone_id': zone_id,
        }
        rs = requests.post(url,headers=headers,data=json.dumps(data))
    return HttpResponse(json.dumps(rs.json()))

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
    container_list_org = rs.json()

    container_list = []
    for container in container_list_org:
        repos = container.pop("repos",None)
        if repos is not None:
            repos = repos.split("/")[-1] 
        container.update({"repos":repos})
        container_list.append(container)
    """get current user role in current project."""
    url='%s/projects/%s' % (BASE_URL,project_id)
    headers={'Content-Type':'application/json'}
    rs = requests.get(url,headers=headers)
    users = rs.json()['users'] 
    project_role=None
    for user in users:
        if user['name'] == user_id:
            project_role = user['role_id']

    return render_to_response('container-table-replace.html',
                             {'container_list':container_list
                              'project_role': project_role})

@require_auth
def stop(request):
    ctn_id = request.GET['id']
    url = '{}/containers/{}/stop'.format(BASE_URL,ctn_id)
    headers={'Content-Type':'application/json'}
    requests.post(url,headers=headers)
    return HttpResponse("succeed")

@require_auth
def start(request):
    ctn_id = request.GET['id']
    url = '{}/containers/{}/start'.format(BASE_URL,ctn_id)
    headers={'Content-Type':'application/json'}
    requests.post(url,headers=headers)
    return HttpResponse("succeed")

@require_auth
def reboot(request):
    ctn_id = request.GET['id']
    url = '{}/containers/{}/reboot'.format(BASE_URL,ctn_id)
    headers={'Content-Type':'application/json'}
    requests.post(url,headers=headers)
    return HttpResponse("succeed")

@require_auth
def commit(request):
    ctn_id = request.GET['id']
    url = '{}/containers/{}/commit'.format(BASE_URL,ctn_id)
    headers={'Content-Type':'application/json'}
    requests.post(url,headers=headers)
    return HttpResponse("succeed")

@require_auth
def destroy(request):
    ctn_nm = request.GET.get('name')
    url = '{}/containers/{}/destroy'.format(BASE_URL,ctn_nm)
    headers={'Content-Type':'application/json'}
    requests.post(url,headers=headers)
    return HttpResponse("succeed")

@require_auth
def refresh(request):
    id = request.GET['id']
    url = '%s/containers/%s/refresh' % ( BASE_URL,id)
    headers = {'Content-Type':'application/json'}
    requests.post(url,headers=headers)
    return HttpResponse("succeed") 
