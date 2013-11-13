var CGI_URL = "http://localhost/cgi-bin/traductor"
var username = "none"
var languagecode = "none"
function onload() {
    document.getElementById("translation_header_block").style.visibility = 'hidden';
}

function login() {
    username = document.getElementsByName("pwd")[0].value;
    var request = {'user': username, 'operation': 'login'};
    send(request);
}

function remove_login_block() {
    var element = document.getElementById("login_block");
    element.parentNode.removeChild(element);
}

function show_translation_header_block() {
    document.body.style.background = "rgb(210,200,247)";
    document.getElementById("translation_header_block").style.visibility = 'visible';
}

function setLanguage(sel) {
    languagecode = sel.options[sel.selectedIndex].value;
    var request = {'user': username, 'operation': 'read', 'data': languagecode};
    send(request);
}

function createLine(name, text, translated_text, translatable) {
    var btn=document.createElement("BUTTON");
    var t=document.createTextNode("CLICK ME");
    btn.appendChild(t);
}

function createLines(json_data) {
    alert(json_data['source'][0]['text']);
    var name = 'line_name';
    var text = 'original text';
    var translated_text = 'translated text';
    var translatable = 'true';    
    createLine(name, text, translated_text, translatable)
}

function destroyLines() {
    document.getElementById("lines_block").innerHTML = '';
}

function send(request) {
    var r = encodeURIComponent(JSON.stringify(request));
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var answer = JSON.parse(xmlhttp.responseText);
            if (answer['error'] == 'true') {
                alert(answer['data']);
            }
            else if (request['operation'] == 'login') {
                remove_login_block();
                show_translation_header_block();
            }
            else if (request['operation'] == 'read') {
                createLines(answer['data']);
            }
        }
    }
    xmlhttp.open("get", CGI_URL+"?"+r, true);
    xmlhttp.send();
}
