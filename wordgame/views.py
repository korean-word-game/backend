from django.shortcuts import render

import uuid
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.core import serializers

from users.forms import LoginForm
from users.models import User
from users.views import check_login
from wordgame.forms import MakeRoomForm
from wordgame.models import Mode
from wordgame.utils import auto_login_controller

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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

    def get(self, req):
        check_login(req)
        isLogin, user = auto_login_controller(req)
        if isLogin is None:
            return redirect('wordgameMain')

        rDict = dict(isLogin=isLogin, now='ingame', user=user)
        return render(req, 'wordgame/ingame.html', rDict)


class wordgameSearch(View):

    def get(self, req, mode):
        check_login(req)
        isLogin, user = auto_login_controller(req)
        if isLogin is None:
            return redirect('wordgameMain')
        if mode == 'classic':
            mode = '클래식'
        elif mode == 'mission':
            mode = '미션'
        else:
            return redirect('wordgameMain')

        rDict = dict(isLogin=isLogin, now='search', user=user, mode=mode, uuid=uuid.uuid4())
        return render(req, 'wordgame/search.html', rDict)


class makeRoom(View):

    def post(self, req):
        check_login(req)
        isLogin, user = auto_login_controller(req)
        if isLogin is None:
            return redirect('wordgameMain')
        room = MakeRoomForm(req.POST)
        room = room.save(commit=True)

        # send room_created event
        room.now_people = 1
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'room_info',
            {'type': 'event_room_created',
             'room_id': room.id,
             'result': serializers.serialize('json', [room])[1:-1]}
        )

        return redirect('room', room.pk)
