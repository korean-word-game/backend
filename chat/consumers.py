# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio

from django.core import serializers
from django.db.models import F

from users.models import User
from wordgame.models import Room
from config.utils import RedisQuery, AioRedisQuery
from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async

ROOM_INFO = 'room_info'
ROOM_PEOPLE_LIMIT = 6
ROOM_EXCEEDED_LIMIT_MSG = '게임에 참가 할 수 없습니다'
ROOM_ALREADY_EXIST_MSG = '이미 게임에 참가 되어있습니다'


class QueryResult:
    @staticmethod
    async def game_status(room_id):
        result = {}

        status, users = await asyncio.gather(
            AioRedisQuery.get_all_game_config(room_id),
            AioRedisQuery.get_room_users(room_id)
        )

        if status:
            result.update(status)
        if users:
            result['users'] = users

        room = Room.objects.get(id=room_id)
        if room:
            result['is_start'] = room.is_start
            result['how_to_win_id'] = room.how_to_win_id
            result['mode_id'] = room.mode_id

        return result


class ChatConsumer(AsyncWebsocketConsumer):
    group_connected = False
    num_increased = False
    room_info = ROOM_INFO
    room_name = room_group_name = user = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        session = self.scope['session']
        if session:
            token = session.get('token')
            if token:
                self.user = User.objects.get(token=token)
                await self.connect_or_raise_if_exceeded_limit()

    async def connect_or_raise_if_exceeded_limit(self):
        if RedisQuery.exist_user(self.room_name, self.user.username):
            await self.accept()
            await self.send_error(ROOM_ALREADY_EXIST_MSG, alert_type=1, action='back')
            await self.disconnect(None)
            await self.close()
            return

        if RedisQuery.room_user_cnt(self.room_name) <= ROOM_PEOPLE_LIMIT:
            try:
                # now_people += 1
                Room.objects.filter(id=self.room_name).update(now_people=F('now_people') + 1)
            except:
                pass
            else:
                self.num_increased = True
                RedisQuery.add_user(self.room_name, self.user.username)

            try:
                # Join room group
                await asyncio.gather(
                    self.channel_layer.group_add(
                        self.room_info,
                        self.channel_name
                    ),
                    self.channel_layer.group_add(
                        self.room_group_name,
                        self.channel_name
                    )
                )
            except:
                await self.disconnect(None)
                return
            else:
                self.group_connected = True

            await self.notice_room_entered()

            await self.accept()

        else:
            await self.accept()
            await self.send_error(ROOM_EXCEEDED_LIMIT_MSG, alert_type=1, action='back')
            await self.disconnect(None)
            await self.close()

    async def notice_room_entered(self):
        await self.channel_layer.group_send(
            self.room_info, {
                'type': 'event_room_entered',
                'room_id': self.room_name,
                'user': self.user.username
            }
        )

    async def notice_room_exit(self):
        await self.channel_layer.group_send(
            self.room_info,
            {
                'type': 'event_room_exit',
                'room_id': self.room_name,
                'user': self.user.username
            }
        )

    async def disconnect(self, close_code):
        if self.num_increased:
            # now_people -= 1
            Room.objects.filter(id=self.room_name).update(now_people=F('now_people') - 1)
            print('pop user!!')
            RedisQuery.pop_user(self.room_name, self.user.username)

        if self.group_connected:
            # notice room exit
            await self.notice_room_exit()

            if self.num_increased:
                await asyncio.sleep(1)  # 1 초를 기다렸는데도
                row = Room.objects.get(id=self.room_name)
                room_id = row.id

                if not row.now_people:  # 사람이 없으면
                    row.delete()  # 방 삭제
                    await self.channel_layer.group_send(
                        self.room_info,
                        {
                            'type': 'event_room_discard',
                            'room_id': room_id
                        }
                    )

            # Leave room group
            await asyncio.gather(
                self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                ),
                self.channel_layer.group_discard(
                    self.room_info,
                    self.channel_name
                )
            )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            print('receive data:', [text_data_json])
            command_type = text_data_json.get('type')

            if command_type == 'chat_message':
                message = text_data_json['message']
                await self.message_send(message)

            elif command_type == 'query':
                query = text_data_json['query']
                callback = text_data_json['callback']

                if query == 'game_status':
                    await self.send_query_result(
                        query,
                        callback,
                        await QueryResult.game_status(self.room_name)
                    )

            # Send message to room group

    async def message_send(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'event_chat_message',
                'message': message,
                'user': self.user.username
            }
        )

    async def send_json(self, json_data):
        print('send data:', json_data)
        # Send message to WebSocket
        await self.send(text_data=json.dumps(json_data))

    async def send_error(self, alert_message, alert_type=1, redirect_url=None, action=None):
        json_data = {
            'type': 'error',
            'alert': alert_message,
            'alert_type': alert_type,
        }
        if redirect_url:
            json_data['redirect'] = redirect_url
        if action:
            json_data['action'] = action

        await self.send_json(json_data)

    async def send_query_result(self, query, callback, result):
        await self.send_json({
            'type': 'query',
            'query': query,
            'callback': callback,
            'result': result
        })

    # Receive message from room group
    async def event_chat_message(self, event):
        await self.send_json({
            'type': 'chat_message',
            'message': event['message'],
            'user': event['user']
        })

    async def event_room_entered(self, event=None):
        await self.channel_layer.send(
            'test-worker',
            {
                'type': 'test_print',
                'text': 'helloo!!!'
            }
        )

        await self.send_json({
            'type': 'room_entered',
            'user': event['user'],
        })

    async def event_room_exit(self, event=None):
        await self.send_json({
            'type': 'room_exit',
            'user': event['user'],
        })

    async def event_room_created(self, event=None):
        return

    async def event_room_discard(self, event=None):
        return


class LobbyConsumer(AsyncWebsocketConsumer):
    room_info = ROOM_INFO
    is_room_info_connected = False

    async def connect(self):
        self.user = None

        token = self.scope['session'].get('token')
        if token:
            self.user = User.objects.get(token=token)

        try:
            # Join room group
            await self.channel_layer.group_add(
                self.room_info,
                self.channel_name
            )
        except:
            pass
        else:
            self.is_room_info_connected = True

            await self.accept()

    async def disconnect(self, close_code):
        if self.is_room_info_connected:
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_info,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            print('[lobby] receive data:', [text_data_json])
            command_type = text_data_json.get('type')

            if command_type == 'query':
                if text_data_json.get('query') == 'get_rooms':
                    await self.event_get_rooms(text_data_json)

            # if command_type == 'chat_message':
            #     message = text_data_json['message']
            #     await self.message_received(message)

            # Send message to room group

    async def send_json(self, json_data):
        print('[lobby] send data:', json_data)
        # Send message to WebSocket
        await self.send(text_data=json.dumps(json_data))

    async def send_room_info_changed(self, room_id, changed_data):
        await self.send_json({
            'type': 'room_info_changed',
            'room_id': room_id,
            'result': changed_data
        })

    async def send_error(self, alert_message, alert_type=1, redirect_url=None, action=None):
        json_data = {
            'type': 'error',
            'alert': alert_message,
            'alert_type': alert_type,
        }
        if redirect_url:
            json_data['redirect'] = redirect_url
        if action:
            json_data['action'] = action

        await self.send_json(json_data)

    async def event_get_rooms(self, event=None):

        filter_str = event.get('filter')

        if filter_str == 'mission':
            models = Room.objects.filter(is_hide=False, mode_id=2)
        elif filter_str == 'classic':
            models = Room.objects.filter(is_hide=False, mode_id=1)
        else:  # None
            models = Room.objects.filter(is_hide=False)

        await self.send_json({
            'type': 'query',
            'query': 'get_rooms',
            'callback': event['callback'],
            'result': serializers.serialize('json', models)
        })

    async def event_room_entered(self, event=None):
        num = Room.objects.get(id=event['room_id']).now_people
        if not num:  # if num!=0
            await self.send_room_info_changed(
                event['room_id'],
                {'now_people': num}
            )

    async def event_room_exit(self, event=None):
        num = Room.objects.get(id=event['room_id']).now_people
        if not num:  # if num!=0
            await self.send_room_info_changed(
                event['room_id'],
                {'now_people': num}
            )

    async def event_room_created(self, event=None):
        await self.send_json({
            'type': 'room_created',
            'result': event['result'],
        })

    async def event_room_discard(self, event=None):
        await self.send_json({
            'type': 'room_discard',
            'room_id': event['room_id'],
        })


if __name__ == '__main__':
    print(async_to_sync(QueryResult.game_status)(13))
