function createXmlHttpRequest(){
        if(window.ActiveXObject){ //如果是IE浏览器  
            return new ActiveXObject("Microsoft.XMLHTTP");  
        }
        else if(window.XMLHttpRequest){ //非IE浏览器  
            return new XMLHttpRequest();  
        }  
}
function addHgDiv()
{
    var newNode=document.createElement("div");
}

function addHg()
{
    var $text = document.getElementById('hgaddr').value;
    if ( $text != ''){
        document.getElementById('hgaddrs').value += $text + "\n";
        document.getElementById('hgaddr').value = '';
    }
}
function addMember()
{
    var $text = document.getElementById('member').value;
    if ( $text != ''){
        document.getElementById('members').value += $text + "\n";
        document.getElementById('member').value = '';
    }
}
$(".project-info").click(function() {
        $('#infoModal').modal('show')
        var $row = $(this).closest("tr");    
        var $text = $row.find(".fp").text();
        var $href = '/projects/detail';
        var $url = $href + "?id=" + $text;
        $.ajax({
            type: "GET",
            url: $url }).done(function( data ) {
                $("#projectInfo").html(data);
        });
        /*$('#filecontent').text($text);
        var $href = $(this).attr("href");
        var xmlHttpRequest;
        xmlHttpRequest = createXmlHttpRequest();
        xmlHttpRequest.onreadystatechange = showFile;
        var $url = $href + "?filepath=" + $text;

        xmlHttpRequest.open("GET",$url,true);
        xmlHttpRequest.send(null);

        function showFile(){
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200){
                var $content = xmlHttpRequest.responseText;
                $('#filecontent').text($content);
            }
        }*/
    });
$(".modify-project").click(function() {
        $('#modifyModal').modal('show');
        var $row = $(this).closest("tr");    
        var $text = $row.find(".fp").text();
        var $href = '/projects/show';
        var $url = $href + "/" + $text;
        var xmlHttpRequest;
        xmlHttpRequest = createXmlHttpRequest();
        xmlHttpRequest.onreadystatechange = showFile;
        xmlHttpRequest.responseType = 'json';
        xmlHttpRequest.open("GET",$url,true);
        xmlHttpRequest.send(null);

        function showFile(){
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200){
                var $content = xmlHttpRequest.response;
                document.getElementById('project_name').value = $content.name;
                document.getElementById('project_desc').value = $content.desc;
                document.getElementById('project_hgs').value = $content.hgs;
                document.getElementById('project_members').value = $content.members;
                document.getElementById('save_modify').value = $text;
            }
        }
});
 
$(".save-modify").click(function() {
        //alert('here');
        var $id = document.getElementById('save_modify').value;
        //var $id = $("#save_button").var();
        //alert($id);
        var $href = "/projects/update";
        var $name = document.getElementById('project_name').value;
        var $desc = document.getElementById('project_desc').value;
        var $members = document.getElementById('project_members').value;
        var $hgs = document.getElementById('project_hgs').value;
        //alert($name);
        var $url = $href + "/" + $id +"?name=" + $name + "&desc=" + $desc  + "&members=" + $members + "&hgs=" + $hgs;
        //alert($url);
        $.ajax({
            type: "GET",
            url: $url }).done(function( data ) {
                window.location.reload();
        });

});
// modify project name 

$(".modify-name").click(function() {
        $('#nameModal').modal('show')
        var $row = $(this).closest("tr");    
        var $text = $row.find(".fp").text();
        var $href = '/projects/show';
        var $url = $href + "/" + $text;
        var xmlHttpRequest;
        xmlHttpRequest = createXmlHttpRequest();
        xmlHttpRequest.onreadystatechange = showFile;
        xmlHttpRequest.responseType = 'json';
        xmlHttpRequest.open("GET",$url,true);
        xmlHttpRequest.send(null);

        function showFile(){
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200){
                var $content = xmlHttpRequest.response;
                //$('#filecontent').text($content);
                document.getElementById('file_name').value = $content.name;
                document.getElementById('save_name').value = $text;
                //$('#file_name').val = 'name';
            }
        }
});        

$(".save-name").click(function() {
        alert('here');
        var $id = document.getElementById('save_name').value;
        //var $id = $("#save_button").var();
        alert($id);
        var $href = "/projects/update";
        var $name = document.getElementById('file_name').value;
        alert($name);
        var $url = $href + "/" + $id +"?name=" + $name + "&desc="  + "&members=" + "&hgs=";
        alert($url);
        $.ajax({
            type: "GET",
            url: $url }).done(function( data ) {
                window.location.reload();
        });
});
// modify project desc 
$(".modify-desc").click(function() {
        $('#descModal').modal('show')
        var $row = $(this).closest("tr");    
        var $text = $row.find(".fp").text();
        var $href = '/projects/show';
        var $url = $href + "/" + $text;
        var xmlHttpRequest;
        xmlHttpRequest = createXmlHttpRequest();
        xmlHttpRequest.onreadystatechange = showFile;
        xmlHttpRequest.responseType = 'json';
        xmlHttpRequest.open("GET",$url,true);
        xmlHttpRequest.send(null);

        function showFile(){
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200){
                var $content = xmlHttpRequest.response;
                document.getElementById('project_desc').value = $content.desc;
                document.getElementById('save_desc').value = $text;
            }
        }
});        

$(".save-desc").click(function() {
        alert('here');
        var $id = document.getElementById('save_desc').value;
        alert($id);
        var $href = "/projects/update";
        var $desc = document.getElementById('project_desc').value;
        alert($desc);
        var $url = $href + "/" + $id +"?name=" + "&desc=" + $desc + "&members=" + "&hgs=";
        alert($url);
        $.ajax({
            type: "GET",
            url: $url }).done(function( data ) {
                window.location.reload();
        });
});

//modify project members 
$(".modify-members").click(function() {
        $('#membersModal').modal('show')
        var $row = $(this).closest("tr");    
        var $text = $row.find(".fp").text();
        var $href = '/projects/show';
        var $url = $href + "/" + $text;
        var xmlHttpRequest;
        xmlHttpRequest = createXmlHttpRequest();
        xmlHttpRequest.onreadystatechange = showFile;
        xmlHttpRequest.responseType = 'json';
        xmlHttpRequest.open("GET",$url,true);
        xmlHttpRequest.send(null);

        function showFile(){
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200){
                var $content = xmlHttpRequest.response;
                document.getElementById('project_members').value = $content.members;
                document.getElementById('save_members').value = $text;
            }
        }
});        

$(".save-members").click(function() {
        alert('here');
        var $id = document.getElementById('save_members').value;
        alert($id);
        var $href = "/projects/update";
        var $members = document.getElementById('project_members').value;
        alert($members);
        var $url = $href + "/" + $id +"?name=" + "&desc=" + "&members=" + $members + "&hgs=";
        alert($url);
        $.ajax({
            type: "GET",
            url: $url }).done(function( data ) {
                window.location.reload();
        });
});

//modify project hgs
$(".modify-hgs").click(function() {
        $('#hgsModal').modal('show')
        var $row = $(this).closest("tr");    
        var $text = $row.find(".fp").text();
        var $href = '/projects/show';
        var $url = $href + "/" + $text;
        var xmlHttpRequest;
        xmlHttpRequest = createXmlHttpRequest();
        xmlHttpRequest.onreadystatechange = showFile;
        xmlHttpRequest.responseType = 'json';
        xmlHttpRequest.open("GET",$url,true);
        xmlHttpRequest.send(null);

        function showFile(){
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200){
                var $content = xmlHttpRequest.response;
                document.getElementById('project_hgs').value = $content.hgs;
                document.getElementById('save_hgs').value = $text;
            }
        }
});        

$(".save-hgs").click(function() {
        alert('here');
        var $id = document.getElementById('save_hgs').value;
        alert($id);
        var $href = "/projects/update";
        var $hgs = document.getElementById('project_hgs').value;
        alert($members);
        var $url = $href + "/" + $id +"?name=" + "&desc=" + "&members=" + "&hgs=" + $hgs;
        alert($url);
        $.ajax({
            type: "GET",
            url: $url }).done(function( data ) {
                window.location.reload();
        });
});




$(".delete-project").click(function() {
        var $row = $(this).closest("tr");    
        var $text = $row.find(".fp").text();
        /*$('#filecontent').text($text);*/
        /*var $href = $(this).attr("href");*/
        var $href= "/projects/delete" 
        var xmlHttpRequest;
        xmlHttpRequest = createXmlHttpRequest();
        xmlHttpRequest.onreadystatechange = getResult;
        var $url = $href + "?id=" + $text;

        xmlHttpRequest.open("GET",$url,true);
        xmlHttpRequest.send(null);

        function getResult(){
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200){
                var $content = xmlHttpRequest.responseText;
                if ($content == 'succeed'){
                    window.location.reload();
                }
            }
        }
});

$("a[href='#projectinfo']").click(function(e) {
      var id = $(this).attr('value');
      var $href = '/projects/detail';
      var $url = $href + '?id=' + id.trim();
      $.ajax({
            type: "GET",
            url: $url }).done(function( data ) {
                $("#projectinfo").html(data);
        });
    });
$("a[href='#projectList']").click(function(e) {
      var name = this.text;
      var $href = '/projects/index';
      var $url = $href; 
      $.ajax({
            type: "GET",
            url: $url }).done(function( data ) {
                $("#projectList").html(data);
        });
    });

$("a[href='#projectList']").on('show.bs.tab', function(e) {
    //alert('shown - after the tab has been shown');
    ;
});

$(document).ready(
    //function () {
    //$("a[href='#projectList']").click();
    document.body.parentNode.style.overflow="hidden";
);

