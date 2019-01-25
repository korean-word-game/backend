import uuid

from django.shortcuts import render

# Create your views here.
from django.utils.safestring import mark_safe
import json

from django.views import View

from users.views import check_login
from wordgame.models import Room
from wordgame.utils import auto_login_controller


def index(request):
    return render(request, 'chat/index.html', {})


class room(View):
    rDict = dict(now='main')

    def get(self, req, room_name):
        check_login(req)
        isLogin, user = auto_login_controller(req)

        rDict = dict(isLogin=isLogin, now='main', user=user, uuid=uuid.uuid4())
        room = Room.objects.get(pk=room_name)
        rDict['room'] = room
        rDict['mode'] = True if room.mode == 2 else False
        return render(req, 'chat/room.html', rDict)
