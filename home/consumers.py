import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Group, GroupMessage, Message
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from django.db.models import Q


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name
        print(self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name,
                                           self.channel_name)
        objs = await self.magrm(self.room_group_name)
        print(objs)

        await self.accept()
        for obj in objs:
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'chat_message',
                    'message': obj['content'],
                    'author': obj['author']
                })

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name,
                                               self.channel_name)

    # Receive message from
    # @database_sync_to_async
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(self.scope['user'])
        # await GroupMessage.objects.create(gname=self.room_group_name,
        #                                   content=message,
        #                                   author=self.scope['user'])
        # Send message to room group
        await self.magrme(self.room_group_name, message, self.scope['user'])
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'author': self.scope['user'].username
            })

    @database_sync_to_async
    def magrme(self, gname, message, user):
        GroupMessage.objects.create(gname=self.room_group_name,
                                    content=message,
                                    author=self.scope['user'])
        return

    @database_sync_to_async
    def magrm(self, gname):
        objs = GroupMessage.objects.filter(gname=self.room_group_name)
        mess = []
        for obj in objs:
            d = {'content': obj.content, 'author': obj.author.username}
            mess.append(d)
        print(mess)
        return mess

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        author = event['author']
        print(event)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author
        }))


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.otheruser = self.scope['url_route']['kwargs']['username']
        ou = await self.getuser(self.otheruser)
        self.room_group_name = str(min(
            ou.id, self.scope['user'].id)) + "userchate" + str(
                max(ou.id, self.scope['user'].id))
        print(self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name,
                                           self.channel_name)
        objs = await self.magrm(self.otheruser)
        # print(objs)

        await self.accept()
        # print("cfrgvjk")
        for obj in objs:
            # print(obj['content'])
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'chat_message',
                    'message': obj['content'],
                    'author': obj['author']
                })

    async def disconnect(self, close_code):
        # print("disconnected")
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name,
                                               self.channel_name)

    # Receive message from
    # @database_sync_to_async
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # print(self.scope['user'].id)
        # await GroupMessage.objects.create(gname=self.room_group_name,
        #                                   content=message,
        #                                   author=self.scope['user'])
        # Send message to room group
        await self.magrme(message, self.otheruser)
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'author': self.scope['user'].username
            })

    @database_sync_to_async
    def magrme(self, message, user):
        print("ygk")
        # print(self.scope['user'].username)
        # print(user)
        # print(message)
        Message.objects.create(From=self.scope['user'],
                               To=user,
                               content=message)
        # print("chvbjh")
        return

    @database_sync_to_async
    def magrm(self, user):
        objs = Message.objects.filter(
            Q(From=self.scope['user'], To=user)
            | Q(From=User.objects.get(username=user),
                To=self.scope['user'].username)).order_by('date')
        mess = []
        for obj in objs:
            d = {'content': obj.content, 'author': obj.From.username}
            mess.append(d)
        # print(mess)
        return mess

    @database_sync_to_async
    def getuser(self, user):
        print("ygk")
        # print(self.scope['user'].username)
        # print(user)
        # print(message)
        return User.objects.get(username=user)
        # print("chvbjh")

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        author = event['author']
        print(event)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author
        }))