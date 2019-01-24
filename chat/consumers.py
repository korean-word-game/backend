# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.core import serializers

from users.models import User
from wordgame.models import Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = None

        token = self.scope['session'].get('token')
        if token:
            self.user = User.objects.get(token=token)

        # await self.get_rooms()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
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
        response_data = {
            'type': 'chat_message',
            'user': self.user.username,
            'message': message
        }
        print('send data:',[response_data])
        await self.channel_layer.group_send(
            self.room_group_name,
            response_data
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def get_rooms(self):
        models = Room.objects.filter(is_hide=False)

        print(serializers.serialize('json', models))
