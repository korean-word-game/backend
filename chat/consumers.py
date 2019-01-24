# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.core import serializers
from django.db.models import F

from users.models import User
from wordgame.models import Room


class ChatConsumer(AsyncWebsocketConsumer):
    group_connected = False
    num_increased = False

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
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                # notice room entered
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'event_room_entered',
                        'user': self.user.username
                    }
                )

                await self.accept()

    async def disconnect(self, close_code):
        if self.num_increased:
            # now_people -= 1
            Room.objects.filter(id=self.room_name).update(now_people=F('now_people') - 1)

        if self.group_connected:
            # notice room exit
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'event_room_exit',
                    'user': self.user.username
                }
            )

            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            print('receive data:', [text_data_json])
            command_type = text_data_json.get('type')

            if command_type == 'chat_message':
                message = text_data_json['message']
                await self.message_received(message)

            # Send message to room group

    async def message_received(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'event_chat_message',
                'message': message,
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
            'user': self.user.username
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
    async def connect(self):
        self.user = None

        token = self.scope['session'].get('token')
        if token:
            self.user = User.objects.get(token=token)

        await self.accept()

    async def disconnect(self, close_code):
        pass

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
