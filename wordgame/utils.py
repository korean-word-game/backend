import re

from django.shortcuts import redirect
from .models import Word, WordType

from users.models import User
import hgtk


def is_hangul(text):
    if re.search('[^가-힣]', text):  # 한글이 아닌 글자가 있으면
        return False
    return True


def auto_login_controller(req):
    user = None
    isLogin = req.session.get('isLogin', False)
    if isLogin:
        ou = User.objects
        try:
            user = ou.get(token=req.session.get('token'))
        except User.DoesNotExist:
            req.session['isLogin'] = False
            return None, None
    return isLogin, user


def search_word(type: int, word):
    word_type = WordType.objects.get(id=type)


def duu(p0, p1):
    p0 = hgtk.letter.decompose(p0[0])
    if p0[0] in ['ㄹ', 'ㄴ', 'ㅇ']:

        if len(p0[2]) == 0:
            p1.append(hgtk.letter.compose('ㄹ', p0[1]))
            p1.append(hgtk.letter.compose('ㄴ', p0[1]))
            p1.append(hgtk.letter.compose('ㅇ', p0[1]))
        else:
            p1.append(hgtk.letter.compose('ㄹ', p0[1], p0[2]))
            p1.append(hgtk.letter.compose('ㄴ', p0[1], p0[2]))
            p1.append(hgtk.letter.compose('ㅇ', p0[1], p0[2]))
