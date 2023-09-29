import asyncio
import httpx
import json
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, HttpResponseServerError
from django.http import JsonResponse

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('fuuuuuuuuuuuuuuuu')
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
       
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = text_data_json["user"]
        id_like = text_data_json["roomName"]
        host = text_data_json["host"]

        addUrl = 'http://{}/apichat/{}/{}/'.format(host, user, id_like)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    addUrl,
                    json={"body": message}
                    )
                if response.status_code == 200:
                    print("API request successful")
            except Exception as e:
                    print(f"An error occurred during the API request: {str(e)}")    
        # Send message to room group
        print("test")
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message, "user":user,}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "user" : user}))