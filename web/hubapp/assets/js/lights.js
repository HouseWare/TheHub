function light_one(on) {
    var xmlhttp;
    var x, state;
    if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
          xmlhttp=new XMLHttpRequest();
      } else {// code for IE6, IE5
          xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
    xmlhttp.onreadystatechange=function() {
          if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            var json = eval('(' + xmlhttp.responseText + ')');
            setdoorLED("led10",json[0].success["/lights/1/state/on"]);
        }
    }

 xmlhttp.open('PUT','http://192.168.2.100/api/hughlightbulb/lights/1/state',true);
    if(on) {
        xmlhttp.send('{"on" : true, "hue" : 50000}');
    } else {
        xmlhttp.send('{"on" : false}');
    }
}

function light_three(on) {
    var xmlhttp;
    var x, state;
    if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
          xmlhttp=new XMLHttpRequest();
      } else {// code for IE6, IE5
          xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
    xmlhttp.onreadystatechange=function() {
          if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            var json = eval('(' + xmlhttp.responseText + ')');
            setdoorLED("led9",json[0].success["/lights/3/state/on"]);
        }
    }

 xmlhttp.open('PUT','http://192.168.2.100/api/hughlightbulb/lights/3/state',true);
    if(on) {
        xmlhttp.send('{"on" : true, "hue" : 65535}');
    } else {
        xmlhttp.send('{"on" : false}');
    }
}
