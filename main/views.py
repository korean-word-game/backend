import json
import uuid
import random
import numpy as np

from django.shortcuts import render
from django.http import JsonResponse
from .models import WordFile, Word, WordType, GameRoom
from django.views.decorators.csrf import csrf_exempt
import time
import hashlib


def get_sha512(p0):
    return hashlib.sha3_512(p0.encode('utf-8')).hexdigest()


def get_token(p0):
    return get_sha512(p0 + ':' + (time.time() * 1000).__int__().__str__())


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
            print('multipart')
        except:
            req_data = json.loads(req.body.decode("utf-8"))
            player = req_data['player']
            print('app/json')
            print(req_data)
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
            token = req_data['token']
            print('multipart')
        except:
            try:
                req_data = json.loads(req.body.decode("utf-8"))
                token = req_data['token']
                print('app/json')
                print(req_data)
            except:
                token = req.session['token']

        word_player = req_data['word']
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
        if len(room.log) != 0 and word_player[0] != before_log[len(before_log) - 1][
            len(before_log[len(before_log) - 1]) - 1]:
            # 왜 끝말을 안쓰시죠?
            return JsonResponse(
                {
                    'success': False,
                    'code': 2
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
        enemy_can = enemy_type.word_set.all()
        for i in range(len(before_log)):
            enemy_can = enemy_can.exclude(text=before_log[i])

        enemy_can = enemy_can.filter(text__startswith=word_player[len(word_player) - 1])

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
            for i in range(len(before_log)):
                player_can = player_can.exclude(text=word_enemy.text[len(word_enemy.text) - 1])

            player_can = player_can.filter(text__startswith=word_player[len(word_player) - 1])

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
            # 널 전적으로 마크해주지
            min_req: int = 99
            min_list = list()
            player_can = player_type.word_set.all()

            for word in enemy_can:
                end = word.text[len(word.text) - 1]
                player_can = player_can.exclude(text=word.text)
                for i in range(len(before_log)):
                    player_can = player_can.exclude(text=word.text[len(word.text) - 1])

                player_can = player_can.filter(text__startswith=end)
                if len(player_can) == min_req:
                    min_list.append(word)
                if len(player_can) < min_req:
                    min_req = len(player_can)
                    min_list = list()
                    min_list.append(word)

            word_enemy = random.choice(min_list)

            # 이건 다음

            before_log.append(word_player)
            before_log.append(word_enemy.text)

            room.log = ','.join(before_log)

            player_can = player_can.exclude(text=word_enemy.text)
            for i in range(len(before_log)):
                player_can = player_can.exclude(text=word_enemy.text[len(word_enemy.text) - 1])

            player_can = player_can.filter(text__startswith=word_player[len(word_player) - 1])

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


@csrf_exempt
def word_search(req):
    if req.method == 'POST':
        try:
            req_data = req.POST
            print('multipart')
        except:
            try:
                req_data = json.loads(req.body.decode("utf-8"))
                token = req_data['token']
                print('app/json')
            except:
                # 토큰은 왜 안보내 마
                return JsonResponse(
                    {
                        'success': False,
                        'code': 0
                    }
                )
