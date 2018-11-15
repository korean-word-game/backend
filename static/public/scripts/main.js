onload = function() {



    var startButton = document.querySelector("#start-button-cover");
    var subButton = document.querySelector("#sub-button-cover");




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
        // alert(results['token']);
        location.href = "/game";
        // alert(getCookie("token"));
    });
    // alert("makeroom끝");
}
    



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
        location.href = "/game";
        // alert(getCookie("token"));
    });
    // alert("makeroom끝");
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
        // alert(results['token']);
        location.href = "/game";
        // alert(getCookie("token"));
    });
    // alert("makeroom끝");
};
    