var CGI_URL = "http://localhost/cgi-bin/traductor";
var debug_lastrequest;
var debug_lastanswer;
var username = "none";
var languagecode = "none";

function onload() {
    document.getElementById("translation_header_block").style.visibility = 'hidden';
    window.setInterval(checkFilledLines, 1000);
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

function createLine(name, text, translated_text, translatable, context) {
    var strong = document.createElement("strong");
    strong.innerHTML = text + " ";
    var small = document.createElement("small");
    small.innerHTML = context;
    var p = document.createElement("p");
    p.appendChild(strong);
    p.appendChild(small);
    var input = document.createElement("input");
    input.setAttribute("type", "text");
    input.setAttribute("value", translated_text);
    input.setAttribute("name", name);
    if (translatable == "false") {
        input.setAttribute("value", text);
        input.setAttribute("readonly", "readonly");
    }
    var lines_block = document.getElementById("lines_block");
    lines_block.appendChild(p);
    lines_block.appendChild(input);
}

function createLines(json_data) {
    number_of_lines_source = json_data['source'].length;
    number_of_lines_translated = json_data[languagecode].length;
    alert(number_of_lines_source + " lines in source and " + number_of_lines_translated + " lines in translation.");
    for (line in json_data['source']) {
        var name = json_data['source'][line]['name'];
        var text = json_data['source'][line]['text'];
        var translatable = json_data['source'][line]['translatable'];
        var translated_text = searchTranslatedText(name, json_data[languagecode]);
        var context = json_data['source'][line]['context'];
        createLine(name, text, translated_text, translatable, context);
    }
}

function searchTranslatedText(name, lines) {
    for (i in lines) {
        if (lines[i]['name'] == name) {
            return lines[i]['text'];
        }
    }
    return "";
}

function destroyLines() {
    document.getElementById("lines_block").innerHTML = '';
}

function writeLines() {
    var lines = [];
    var inputs = document.getElementsByTagName("input");
    for (i in inputs) {
        if (inputs[i].type == "text") {
            var name = inputs[i].name;
            var translated_text = inputs[i].value;
            lines.push({'name': name, 'text': translated_text});
        }
    }
    var data = {'language_code': languagecode, 'lines': lines};
    var request = {'user': username, 'operation': 'write', 'data': data};
    send(request);
}

function checkFilledLines() {
    var inputs = document.getElementsByTagName("input");
    for (i in inputs) {
        if (inputs[i].type == "text" && inputs[i].value == "") {
            inputs[i].setAttribute("class", "incomplete");
        }
        else if (inputs[i].type == "text") {
            inputs[i].setAttribute("class", "done");
        }
    }
}

function send(request) {
    var r = encodeURIComponent(JSON.stringify(request));
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            debug_lastanswer = xmlhttp.responseText;
            var answer = JSON.parse(xmlhttp.responseText);
            if (answer['error'] == 'true') {
                alert(answer['data']);
            }
            else if (request['operation'] == 'login') {
                remove_login_block();
                show_translation_header_block();
            }
            else if (request['operation'] == 'read') {
                destroyLines();
                createLines(answer['data']);
            }
            else if (request['operation'] == 'write') {
                alert(answer['data']);
            }
        }
    }
    debug_lastrequest = CGI_URL+"?"+r;
    xmlhttp.open("get", CGI_URL+"?"+r, true);
    xmlhttp.send();
}
