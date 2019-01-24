# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio

from django.core import serializers
from django.db.models import F

from users.models import User
from wordgame.models import Room

LOBBY_GROUP_NAME = 'lobby'


class ChatConsumer(AsyncWebsocketConsumer):
    group_connected = False
    num_increased = False
    lobby_group_name = LOBBY_GROUP_NAME

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = None

        session = self.scope['session']
        if session:
            token = session.get('token')
            if token:
                self.user = User.objects.get(token=token)
                self.group_connected = True

                try:
                    # now_people += 1
                    Room.objects.filter(id=self.room_name).update(now_people=F('now_people') + 1)
                except:
                    pass
                else:
                    self.num_increased = True

                # Join room group
                await asyncio.gather(
                    self.channel_layer.group_add(
                        self.room_group_name,
                        self.channel_name
                    ),
                    self.channel_layer.group_add(
                        self.lobby_group_name,
                        self.channel_name
                    )
                )

                await self.notice_room_entered()

                await self.accept()

    async def notice_room_entered(self):
        await asyncio.gather(
            self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'event_room_entered',
                    'user': self.user.username
                }
            ),
            self.channel_layer.group_send(
                self.lobby_group_name, {
                    'type': 'event_room_entered',
                    'room_id': self.room_name
                }
            )
        )

    async def notice_room_exit(self):

        await asyncio.gather(
            self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'event_room_exit',
                    'user': self.user.username
                }
            ), self.channel_layer.group_send(
                self.lobby_group_name,
                {
                    'type': 'event_room_exit',
                    'room_id': self.room_name,
                }
            )
        )

    async def disconnect(self, close_code):
        if self.num_increased:
            # now_people -= 1
            Room.objects.filter(id=self.room_name).update(now_people=F('now_people') - 1)

        if self.group_connected:
            # notice room exit
            await self.notice_room_exit()

            # Leave room group
            await asyncio.gather(
                self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                ),
                self.channel_layer.group_discard(
                    self.lobby_group_name,
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

    # Receive message from room group
    async def event_chat_message(self, event):
        await self.send_json({
            'type': 'chat_message',
            'message': event['message'],
            'user': event['user']
        })

    async def event_get_rooms(self, event=None):
        models = Room.objects.filter(is_hide=False)

        print(serializers.serialize('json', models))

    async def event_room_entered(self, event=None):
        await self.send_json({
            'type': 'room_entered',
            'user': event['user'],
        })

    async def event_room_exit(self, event=None):
        await self.send_json({
            'type': 'room_exit',
            'user': event['user'],
        })


class LobbyConsumer(AsyncWebsocketConsumer):
    lobby_group_name = LOBBY_GROUP_NAME

    async def connect(self):
        self.user = None

        token = self.scope['session'].get('token')
        if token:
            self.user = User.objects.get(token=token)

        # Join room group
        await self.channel_layer.group_add(
            self.lobby_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.lobby_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            print('receive data:', [text_data_json])
            command_type = text_data_json.get('type')

            if command_type == 'query':
                if text_data_json.get('query') == 'get_rooms':
                    await self.event_get_rooms(text_data_json)

            # if command_type == 'chat_message':
            #     message = text_data_json['message']
            #     await self.message_received(message)

            # Send message to room group

    async def send_json(self, json_data):
        print('send data:', json_data)
        # Send message to WebSocket
        await self.send(text_data=json.dumps(json_data))

    async def send_room_info_changed(self, room_id, changed_data):
        await self.send_json({
            'type': 'room_info_changed',
            'room_id': room_id,
            'result': changed_data
        })

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
        await self.send_room_info_changed(
            event['room_id'],
            {'now_people': Room.objects.get(id=event['room_id']).now_people}
        )

    async def event_room_exit(self, event=None):
        await self.send_room_info_changed(
            event['room_id'],
            {'now_people': Room.objects.get(id=event['room_id']).now_people}
        )
