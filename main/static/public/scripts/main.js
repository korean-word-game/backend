onload = function() {













}

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);
});

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems);
});





function makeroom() {

    let path;
    let results;
    // alert("makeroom이 실행은 됨");
    path = fetch("/api/makeroom/", {
        method: "post",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: JSON.stringify({
            "player": 2,
            "enemy": 1,
            "level": 0,
            "start": 1
        })
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (myJSON) {
        results = myJSON;
        // alert(results.success);
        setCookie("token", results['token'], 1);
        // alert(results['token']);
        location.href = "/game";
        // alert(getCookie("token"));
    });
    // alert("makeroom끝");
    


    function setCookie(cookie_name, value, days) {
        var exdate = new Date();
        exdate.setDate(exdate.getDate() + days);
        // 설정 일수만큼 현재시간에 만료값으로 지정
      
        var cookie_value = escape(value) + ((days == null) ? '' : ';    expires=' + exdate.toUTCString());
        document.cookie = cookie_name + '=' + cookie_value;
    }
};



function makeroomLuck() {

    let path;
    let results;
    // alert("makeroom이 실행은 됨");
    path = fetch("/api/makeroom/", {
        method: "post",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: JSON.stringify({
            "player": 2,
            "enemy": 1,
            "level": 1,
            "start": 1
        })
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (myJSON) {
        results = myJSON;
        // alert(results.success);
        setCookie("token", results['token'], 1);
        // alert(results['token']);
        location.href = "/game";
        // alert(getCookie("token"));
    });
    // alert("makeroom끝");
    


    function setCookie(cookie_name, value, days) {
        var exdate = new Date();
        exdate.setDate(exdate.getDate() + days);
        // 설정 일수만큼 현재시간에 만료값으로 지정
      
        var cookie_value = escape(value) + ((days == null) ? '' : ';    expires=' + exdate.toUTCString());
        document.cookie = cookie_name + '=' + cookie_value;
    }
};



function makeroomFuck() {

    let path;
    let results;
    // alert("makeroom이 실행은 됨");
    path = fetch("/api/makeroom/", {
        method: "post",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: JSON.stringify({
            "player": 2,
            "enemy": 1,
            "level": 2,
            "start": 1
        })
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (myJSON) {
        results = myJSON;
        // alert(results.success);
        setCookie("token", results['token'], 1);
        // alert(results['token']);
        location.href = "/game";
        // alert(getCookie("token"));
    });
    // alert("makeroom끝");
    


    function setCookie(cookie_name, value, days) {
        var exdate = new Date();
        exdate.setDate(exdate.getDate() + days);
        // 설정 일수만큼 현재시간에 만료값으로 지정
      
        var cookie_value = escape(value) + ((days == null) ? '' : ';    expires=' + exdate.toUTCString());
        document.cookie = cookie_name + '=' + cookie_value;
    }
};




function getCookie(cookie_name) {
    var x, y;
    var val = document.cookie.split(';');

    for (var i = 0; i < val.length; i++) {
        x = val[i].substr(0, val[i].indexOf('='));
        y = val[i].substr(val[i].indexOf('=') + 1);
        x = x.replace(/^\s+|\s+$/g, ''); // 앞과 뒤의 공백 제거하기
        if (x == cookie_name) {
        return unescape(y); // unescape로 디코딩 후 값 리턴
        }
    }
}