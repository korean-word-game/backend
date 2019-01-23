from django.shortcuts import render, redirect
from django.views import View

from users.exceptions import SameError, PasswordNotMatchError
from users.models import User
from .forms import LoginForm, RegisterForm


def check_login(p0):
    if p0.session.get('isLogin', False):
        return redirect('idolMain')


class Logout(View):
    def get(self, req):
        req.session['isLogin'] = False
        return redirect('idolMain')


class Login(View):
    rDict = dict(now='login')

    def get(self, req):
        check_login(req)
        return render(req, 'account/login.html', self.rDict)

    def post(self, req):
        try:
            user = LoginForm(req.POST)
            user = user.get_user()
            req.session['isLogin'] = True
            req.session['token'] = user.token
            return redirect('idolMain')

        except User.DoesNotExist:
            self.rDict['error'] = '정확한 정보를 입력해주세요'
            return render(req, 'account/login.html', self.rDict)


class Register(View):
    rDict = dict(now='register')

    def get(self, req):
        check_login(req)
        return render(req, 'account/signup.html', self.rDict)

    def post(self, req):
        try:
            user = RegisterForm(req.POST)
            user = user.save()
            req.session['isLogin'] = True
            req.session['token'] = user.token
            return redirect('idolMain')
        except ValueError:
            self.rDict['error'] = '제데로 된 정보를 입력해주세요.'
        except (SameError, PasswordNotMatchError) as e:
            self.rDict['error'] = e.msg
        finally:
            return render(req, 'account/signup.html', self.rDict)


