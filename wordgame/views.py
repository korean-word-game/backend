from django.shortcuts import render

from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from users.forms import LoginForm
from users.models import User
from users.views import check_login
from wordgame.utils import auto_login_controller


# Create your views here.

class wordgameMain(View):
    rDict = dict(now='main')

    def get(self, req):
        check_login(req)
        isLogin, user = auto_login_controller(req)
        if isLogin is None:
            return redirect('wordgameMain')

        rDict = dict(isLogin=isLogin, now='main', user=user)
        return render(req, 'wordgame/main.html', rDict)

    def post(self, req):
        try:
            user = LoginForm(req.POST)
            user = user.get_user()
            req.session['isLogin'] = True
            req.session['token'] = user.token
            return redirect('wordgameMain')

        except User.DoesNotExist:
            isLogin, user = auto_login_controller(req)
            self.rDict['isLogin'] = isLogin
            self.rDict['user'] = user
            self.rDict['error'] = '정확한 정보를 입력해주세요'

            return render(req, 'wordgame/main.html', self.rDict)


class wordgameIngame(View):
    rDict = dict(now='main')

    def get(self, req):
        check_login(req)
        isLogin, user = auto_login_controller(req)

        rDict = dict(isLogin=isLogin, now='main', user=user)
        return render(req, 'wordgame/ingame.html', rDict)

