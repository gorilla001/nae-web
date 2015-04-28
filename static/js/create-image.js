
function createImage()
{
    var project_id = "id" 
    var repo_path = document.getElementById('repo_path').value;
    var image_desc = document.getElementById('image_desc').value;

    alert(project_id);
    var http = new createXmlHttpRequest();
    var url ="/images/create/";
    var params = "project_id=" + project_id + "&image_desc=" + image_desc + "&repo_path=" + repo_path ;
    var token = '{{ csrf_token }}'; 
    
    alert(token);
    http.open("POST",url,true);
    http.setRequestHeader('X-CSRFToken', token);
    http.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    http.setRequestHeader("Content-length",params.length);
    http.setRequestHeader("Connection", "close");
    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) {
            //var status = http.response.status;
            var content = http.response;
            var status = http.response.status; 
            if (status == 200){
                $.notify("创建成功", "success");
            }
            window.location.reload();
        }
    }
    http.responseType = 'json';
    http.send(params);
}
