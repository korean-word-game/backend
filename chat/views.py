from django.shortcuts import render

# Create your views here.
from django.utils.safestring import mark_safe
import json

from django.views import View

from users.views import check_login
from wordgame.utils import auto_login_controller


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


class Room(View):
    rDict = dict(now='main')

    def get(self, req, room_name):
        check_login(req)
        isLogin, user = auto_login_controller(req)

        rDict = dict(isLogin=isLogin, now='main', user=user)
        rDict['room_name']=mark_safe(json.dumps(room_name))
        return render(req, 'chat/room.html', rDict)
