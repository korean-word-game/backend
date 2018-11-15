var temp;
let log="";
function send() {
    if ((document.querySelector("#send-word").value) == "gg" || (document.querySelector("#send-word").value) == "ㅈㅈ" || (document.querySelector("#send-word").value) == "ㅉ") {
        location.href = "/";
        return 0;
    }
    // 왼쪽, box-in에 기록, box-temp 삭제
    (document.querySelector("#game-bg")).classList.add("to-left");
    document.querySelector("#record-box-in").textContent = log;
    (document.querySelector("#record-box-temp")).textContent = "";
    
    // 복귀,
    setTimeout(function () {
        (document.querySelector("#game-bg")).classList.remove("to-left");
    }, 100);

    // 오른쪽, game-main 오른쪽으로
    setTimeout(function () {
        (document.querySelector("#game-bg")).classList.add("to-right");
        (document.querySelector("#send-word")).classList.add("text-align-right");
    }, 200);

    // 복귀
    setTimeout(function () {
        (document.querySelector("#game-bg")).classList.remove("to-right");
    }, 300);

    // 위쪽, game-main사라지고 원상복귀, box-temp로 이동
    setTimeout(function () {
        (document.querySelector("#game-bg")).classList.add("to-top");
        temp = (document.querySelector("#send-word")).value;
        (document.querySelector("#send-word")).value = "";
        (document.querySelector("#send-word")).classList.remove("text-align-right");
        (document.querySelector("#record-box-temp")).textContent = temp;
    }, 400);

    // 복귀
    setTimeout(function () {
        (document.querySelector("#game-bg")).classList.remove("to-top");
    }, 500);

    // 왼쪽, box-temp 를 box-in에 넣음
    setTimeout(function () {
        (document.querySelector("#game-bg")).classList.add("to-left");
        (document.querySelector("#record-box-in")).textContent += ' -> '+ (document.querySelector("#record-box-temp").textContent);
        (document.querySelector("#record-box-temp")).textContent = "";
    }, 600);

    // 복귀
    setTimeout(function () {
        (document.querySelector("#game-bg")).classList.remove("to-left");
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
            "word": word
        })
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (myJSON) {
        results = myJSON;
        let resultsWord;
        if (results.word != undefined) {
            resultsWord = results.word;
        }
        (document.querySelector("#meaning-box > div")).textContent = results.info;
        (document.querySelector("#meaning-box > h6 > b")).textContent = results.word;
        log = results.log;

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

        // 아래쪽, bubble에 컴퓨터 단어 추가
        setTimeout(function () {
            (document.querySelector("#game-bg")).classList.add("to-bottom");
            M.toast({html: resultsWord});
            (document.querySelector("#speech-bubble")).textContent = resultsWord;
        }, 800);

        // 복귀
        setTimeout(function () {
            (document.querySelector("#game-bg")).classList.remove("to-bottom");
        }, 900);

        // 오른쪽, bubble의 글자 정렬 오른쪽으로
        setTimeout(function () {
            (document.querySelector("#game-bg")).classList.add("to-right");
            (document.querySelector("#speech-bubble")).classList.add("text-align-right");
        }, 1000);

        // 복귀
        setTimeout(function () {
            (document.querySelector("#game-bg")).classList.remove("to-right");
        }, 1100);

        // 아래쪽, bubble의 글을 box-temp로
        setTimeout(function () {
            (document.querySelector("#game-bg")).classList.add("to-bottom");
            (document.querySelector("#speech-bubble")).value = "";
            (document.querySelector("#speech-bubble")).classList.remove("text-align-right");
            (document.querySelector("#record-box-temp")).textContent = resultsWord;
            (document.querySelector("#record-box-in")).scrollTop = (document.querySelector("#record-box-in")).scrollHeight;
        }, 1200);

        // 복귀
        setTimeout(function () {
            (document.querySelector("#game-bg")).classList.remove("to-bottom");
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
        }, 1300);




    });

}
