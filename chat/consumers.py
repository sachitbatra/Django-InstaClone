import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import ChatMessage, Thread
from authentication.models import UserSessionToken
from authentication.views import check_token_ttl

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)

        session_token = self.scope.get("session").get("session_token", None)
        await self.get_user(session_token)

        other_user = self.scope['url_route']['kwargs']['email']

        thread_object = await self.get_thread(self.curUser, other_user)
        self.thread_object = thread_object

        chat_room = f"thread_{thread_object.id}"
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("receive", event)

        front_text = event.get('text', None)
        if front_text is not None:
            loaded_data = json.loads(front_text)
            msg_text = loaded_data.get('message', None)

            msg_response = {
                'message': msg_text,
                'username': self.curUser.name,
                'email_address':self.curUser.email_address
            }

            await self.create_chat_message(self.curUser, msg_text)

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",
                    "text": json.dumps(msg_response)
                }
            )

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def get_thread(self, user, other_user):  # get_or_create
        return Thread.objects.get_or_new(user, other_user)[0]

    @database_sync_to_async
    def create_chat_message(self, user, message):
        return ChatMessage.objects.create(thread=self.thread_object, user=user, message=message)

    @database_sync_to_async
    def get_user(self, session_token):
        sessionDB = UserSessionToken.objects.filter(session_token=session_token).first()
        self.curUser = sessionDB.user
