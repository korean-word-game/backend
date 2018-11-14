# 북한말 남한말 끝말잇기 서버

## 개요

> 끝말잇기로 서로의 단어를 잇는것을 넘어 남북한을 통일의 길로 이어줄 남북한 단어 끝말잇기 서비스 입니다.

## 사용법


1. git clone "https://github.com/korean-word-game/backend.git"<br><br>
2. cd backend<br><br>
3. mkdir .config_secret<br><br>
4. 아래와 같이 프로젝트 루트에 파일 생성<br><br>
 .config_secret<br>
┣━━━ settings_common.json<br>
┣━━━ settings_debug.json<br>
┗━━━ settings_deploy.json<br><br><pre>
settings_common.json<br><br><code>{
  "django": {
    "secret_key": 장고 KEY값,
    "database": DB정보
  }
}
</code><br>
settings_debug.json<br><br><code>{
  "django": {
    "allowed_hosts": [
      테스트용 호스트
    ]
  }
}
</code><br>
settings_deploy.json<br><br><code>{
  "django": {
    "allowed_hosts": [
      서빙용 호스트
    ]
  }
}
</code>
</pre>5. 마이그레이션 등등 설정...<br><br>
6. 디버깅용 옵션 --settings=koreanwordgame.settings.debug <br>
실서비스용 옵션 --settings=koreanwordgame.settings.deploy