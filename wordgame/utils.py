from django.shortcuts import redirect

from users.models import User


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
