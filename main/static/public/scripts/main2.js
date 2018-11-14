var temp;
function send() {
    if ((document.querySelector("#send-word").value) == "gg" || (document.querySelector("#send-word").value) == "ㅈㅈ") {
        location.href = "/";
        return 0;
    }
    (document.querySelector("body")).classList.add("to-right");
    (document.querySelector("#send-word")).classList.add("text-align-right");
    setTimeout(function () {
        (document.querySelector("body")).classList.remove("to-right");
    }, 100);
    setTimeout(function () {
        (document.querySelector("body")).classList.add("to-top");
        temp = (document.querySelector("#send-word")).value;
        (document.querySelector("#send-word")).classList.remove("text-align-right");
        (document.querySelector("#send-word")).value = "";
        (document.querySelector("#record-box-temp")).textContent = temp;
    }, 300);
    setTimeout(function () {
        (document.querySelector("body")).classList.remove("to-top");
    }, 400);
    setTimeout(function () {
        (document.querySelector("body")).classList.add("to-left");
        (document.querySelector("#record-box-temp")).textContent = "";
        (document.querySelector("#record-box-in")).textContent += (temp + " - ");
    }, 600);
    setTimeout(function () {
        (document.querySelector("body")).classList.remove("to-left");
    }, 700);
    

    let path;
    let word = (document.querySelector("#send-word")).value;
    let results;
    M.toast({html: word});
    path = fetch("/api/playgame/", {
        method: "post",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: JSON.stringify({
            "word": word,
            "token": getCookie("token")
        })
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (myJSON) {
        results = myJSON;
        if (results.word != undefined) {
            resultsWord = results.word;
        }
        (document.querySelector("#meaning-box > div")).textContent = results.info;
        (document.querySelector("#meaning-box > h6 > b")).textContent = results.word;
        if (!results.success) {
            switch(results.code) {
                case 0:
                    M.toast({html: "한글만 입력하세요!"});
                    break;
                case 1:
                    M.toast({html: "두글자 이상 입력하세요!"});
                    break;
                case 2:
                    M.toast({html: "제대로 끝말을 이으세요!"});
                    break;
                case 3:
                    M.toast({html: "이미 나온 단어입니다!"});
                    break;
                case 4:
                    M.toast({html: "없는 단어입니다!"});
                    break;
                case 5:
                    M.toast({html: "시작 한방단어 금지"});
                    break;
                default:
                    alert("치명적 오류 치명적 오류 치명적 오류 치명적 오류 치명적 오류 치명적 오류 치명적 오류 치명적 오류 치명적 오류 치명적 오류 치명적 오류 치명적 오류");
            }
        }


        setTimeout(function () {
            M.toast({html: resultsWord});
            (document.querySelector("#speech-bubble")).textContent = resultsWord;
        }, 700);
        setTimeout(function () {
            (document.querySelector("body")).classList.add("to-buttom");
            (document.querySelector("#record-box-temp")).textContent = resultsWord;
            (document.querySelector("#speech-bubble")).textContent = "";
        }, 900);
        setTimeout(function () {
            (document.querySelector("body")).classList.remove("to-buttom");
        }, 1000)
        
        setTimeout(function () {
            (document.querySelector("body")).classList.add("to-left");
            (document.querySelector("#record-box-temp")).textContent = "";
                (document.querySelector("#record-box-in")).textContent += (resultsWord + " - ");
        }, 1100);
        setTimeout(function () {
            (document.querySelector("body")).classList.remove("to-left");
            if(results.finish) {
                if (results.win == "cpu") {
                    alert("컴퓨터가 이겼습니다!");
                    M.toast({html: "컴퓨터가 이겼습니다!"});
                    location.href = "/";
                    return 0;
                } else {
                    alert("당신이 이겼습니다!");
                    M.toast({html: "당신이 이겼습니다!"});
                    location.href = "/";
                    return 0;
                }
            }
        }, 1200);
    });

}

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