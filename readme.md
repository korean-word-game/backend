# 북한말 남한말 끝말잇기 서버

## Summary

> 끝말잇기로 서로의 단어를 잇는것을 넘어 남북한을 통일의 길로 이어줄 남북한 단어 끝말잇기 서비스 입니다.

## Configuration

```
.config_secret
 ┣━━━ settings_common.json
 ┣━━━ settings_debug.json
 ┗━━━ settings_deploy.json
```

<br/>

**settings_common.json**

```
{
  "django": {
    "secret_key": DJANGO_SECRET_KEY,
    "database": DB_URI
  }
}
```

**settings_debug.json**

```
{
  "django": {
    "allowed_hosts": [테스트용 호스트]
  }
}
```

**settings_deploy.json**

```
{
  "django": {
    "allowed_hosts": [서빙용 호스트]
  }
}
```

## Django run options
- for debug:      `--settings=koreanwordgame.settings.debug`
- for production: `--settings=koreanwordgame.settings.deploy`
