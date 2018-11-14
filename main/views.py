import json
import uuid
import random
import numpy as np
import hgtk

from django.shortcuts import render
from django.http import JsonResponse
from .models import WordFile, Word, WordType, GameRoom
from django.views.decorators.csrf import csrf_exempt
import time
import hashlib

import re


def isHangul(text):
    encText = text

    hanCount = len(re.findall(u'^[가-힣]+$', encText))
    return hanCount > 0


def get_sha512(p0):
    return hashlib.sha3_512(p0.encode('utf-8')).hexdigest()


def get_token(p0):
    return get_sha512(p0 + ':' + (time.time() * 1000).__int__().__str__())


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

def index(req):
    if req.method == 'GET':
        return render(req, 'views/index.html', {})

def game1(req):
    if req.method == 'GET':
        return render(req, 'views/game1.html', {})

@csrf_exempt
def word_plus(req):
    if req.method == 'POST':
        req_data = req.POST
        word_file = WordFile(file=req.FILES['file'])
        word_file.save()
        path = "media/" + word_file.file.name
        with open(path) as fr:
            word_data = json.load(fr)

        data_type = WordType.objects.get(id=req_data['type'])
        ob = Word.objects
        for word in word_data:
            if word[1] == "명사":
                word_sample = word[0].replace('-', '')

                if len(word_sample) <= 1 or ob.filter(type=data_type).filter(text=word_sample).exists():
                    continue

                temp = Word(type=data_type, text=word_sample, info=word[2], rank=0)
                temp.save()

        return JsonResponse({'success': True})


@csrf_exempt
def make_room(req):
    if req.method == 'POST':
        try:
            req_data = req.POST
            player = req_data['player']
        except:
            req_data = json.loads(req.body.decode("utf-8"))
            player = req_data['player']
        enemy = req_data['enemy']
        level = req_data['level']

        uid = uuid.uuid4()

        token = get_token(uid.urn.__str__())
        req.session['token'] = token

        if str(req_data['start']) == '0':
            room = GameRoom(token=token, player=player, enemy=enemy, level=int(level),
                            start=0)
            room.save()
            enemy_type = WordType.objects.get(id=room.enemy)
            enemy_can = enemy_type.word_set.all()
            word_enemy = np.random.choice(enemy_can)
            room.log = word_enemy.text
            room.save()
            return JsonResponse(
                {
                    'success': True,
                    'token': token,
                    'word': word_enemy.text
                }
            )
        elif str(req_data['start']) == '1':
            room = GameRoom(token=token, player=player, enemy=enemy, level=int(level),
                            start=1)
            room.save()
            return JsonResponse(
                {
                    'success': True,
                    'token': token
                }
            )


@csrf_exempt
def word_game(req):
    if req.method == 'POST':
        try:
            req_data = req.POST
            word_player = req_data['word']
        except:
            req_data = json.loads(req.body.decode("utf-8"))
            word_player = req_data['word']

        token = req.session['token']
        print(isHangul(word_player))
        if not isHangul(word_player):
            # 한글자 이하
            return JsonResponse(
                {
                    'success': False,
                    'code': 0
                }
            )

        room = GameRoom.objects.get(token=token)
        before_log = room.log.split(',')
        player_type = WordType.objects.get(id=room.player)
        enemy_type = WordType.objects.get(id=room.enemy)



        if len(word_player) <= 1:
            # 한글자 이하
            return JsonResponse(
                {
                    'success': False,
                    'code': 1
                }
            )
        du = list()
        duu(word_player, du)

        du_next = list()
        duu(word_player[len(word_player) - 1], du_next)
        if len(room.log) != 0:
            end_word = before_log[len(before_log) - 1][len(before_log[len(before_log) - 1]) - 1]
            if (not (end_word in du)) and end_word != word_player[0]:
                # 왜 끝말을 안쓰시죠?
                return JsonResponse(
                    {
                        'success': False,
                        'code': 2
                    }
                )
        else:
            if not enemy_type.word_set.filter(text__startswith=word_player[len(word_player) - 1]).exists():
                # 응 처음엔 한방 쓰지
                return JsonResponse(
                    {
                        'success': False,
                        'code': 5
                    }
                )
        if word_player in before_log:
            # 이미 나왔는데수웅
            return JsonResponse(
                {
                    'success': False,
                    'code': 3
                }
            )

        if not player_type.word_set.filter(text=word_player).exists():
            # 근데 그런 단어는 없는데수웅?
            return JsonResponse(
                {
                    'success': False,
                    'code': 4
                }
            )

        # 이제 플레이어를 이겨봅시다
        enemy_ob = enemy_type.word_set
        enemy_can = enemy_ob.all()
        for i in range(len(before_log)):
            enemy_can = enemy_can.exclude(text=before_log[i])

        if len(du_next) != 0:
            enemy_can = enemy_ob.filter(text__startswith=du_next[0]) | enemy_ob.filter(
                text__startswith=du_next[1]) | enemy_ob.filter(text__startswith=du_next[2])
        else:
            enemy_can = enemy_ob.filter(text__startswith=word_player[len(word_player) - 1])

        if not enemy_can.exists():
            return JsonResponse(
                {
                    'success': True,
                    'finish': True,
                    'win': 'player'
                }
            )

        if room.level == 0:
            # 랜덤으로 뽑는 호구봇
            word_enemy = random.choice(enemy_can)

            before_log.append(word_player)
            before_log.append(word_enemy.text)

            room.log = ','.join(before_log)

            player_can = player_type.word_set.all()
            player_can = player_can.exclude(text=word_enemy.text)

            player_can = player_can.filter(text__startswith=word_enemy.text[len(word_enemy.text) - 1])
            for i in before_log:
                player_can = player_can.exclude(text=i)
            room.save()

            if not player_can.exists():
                return JsonResponse(
                    {
                        'success': True,
                        'finish': True,
                        'word': word_enemy.text,
                        'info': word_enemy.info,
                        'win': 'cpu'
                    }
                )

            return JsonResponse(
                {
                    'success': True,
                    'finish': False,
                    'word': word_enemy.text,
                    'info': word_enemy.info
                }
            )
        elif room.level == 1:
            # 반박할게 100개 미만이야 나감
            player_ob = player_type.word_set.all()
            for _ in range(10):
                word_enemy = random.choice(enemy_can)

                du_tmp = list()
                duu(word_enemy.text[len(word_enemy.text) - 1], du_tmp)
                player_can = player_ob.exclude(text=word_enemy.text)
                if len(du_tmp) != 0:
                    player_can = player_can.filter(text__startswith=du_tmp[0]) | player_can.filter(
                        text__startswith=du_tmp[1]) | player_can.filter(text__startswith=du_tmp[2])
                else:
                    player_can = player_can.filter(text__startswith=word_enemy.text[len(word_enemy.text) - 1])

                for i in before_log:
                    player_can = player_can.exclude(text=i)
                if len(player_can) <= 400:
                    break
            else:
                word_enemy = random.choice(enemy_can)


            before_log.append(word_player)
            before_log.append(word_enemy.text)

            room.log = ','.join(before_log)
            room.save()
            print(player_can)

            if not player_can.exists():
                return JsonResponse(
                    {
                        'success': True,
                        'finish': True,
                        'word': word_enemy.text,
                        'info': word_enemy.info,
                        'win': 'cpu'
                    }
                )

            return JsonResponse(
                {
                    'success': True,
                    'finish': False,
                    'word': word_enemy.text,
                    'info': word_enemy.info
                }
            )
        elif room.level == 2:
            # 널 전적으로 마크해주지
            min_req: int = 12312312312
            min_list = list()
            player_ob = player_type.word_set.all()
            for i in before_log:
                player_ob = player_ob.exclude(text=i)

            for word in enemy_can:
                end = word.text[len(word.text) - 1]

                du_tmp = list()
                duu(word.text[len(word.text)-1], du_tmp)
                player_can = player_ob.exclude(text=word.text)

                if len(du_tmp) != 0:
                    player_can = player_can.filter(text__startswith=du_tmp[0]) | player_can.filter(
                        text__startswith=du_tmp[1]) | player_can.filter(text__startswith=du_tmp[2])
                else:
                    player_can = player_can.filter(text__startswith=end)
                if len(player_can) == min_req:
                    min_list.append(word)
                if len(player_can) < min_req:
                    min_req = len(player_can)
                    min_list = list()
                    min_list.append(word)
                if 0 == min_req:
                    return JsonResponse(
                        {
                            'success': True,
                            'finish': True,
                            'word': word.text,
                            'info': word.info,
                            'win': 'cpu'
                        }
                    )

            word_enemy = random.choice(min_list)

            # 이건 다음
            before_log.append(word_player)
            before_log.append(word_enemy.text)

            room.save()

            return JsonResponse(
                {
                    'success': True,
                    'finish': False,
                    'word': word_enemy.text,
                    'info': word_enemy.info
                }
            )
