from channels.generic.websocket import AsyncWebsocketConsumer

import json

class NotificationConsumer(AsyncWebsocketConsumer):
    
    # Function to connect to the websocket
    async def connect(self):
       # Checking if the User is logged in
        if self.scope["user"].is_anonymous:
            # Reject the connection
            self.close()
        else:
            # print(self.scope["user"])   # Can access logged in user details by using self.scope.user, Can only be used if AuthMiddlewareStack is used in the routing.py
            # self.group_name = str(self.scope["user"].pk)  # Setting the group name as the pk of the user primary key as it is unique to each user. The group name is used to communicate with the user.
            self.group_name = "Notification_Group"  # Setting the group name as the pk of the user primary key as it is unique to each user. The group name is used to communicate with the user.
           
            await self.channel_layer.group_add(
                self.group_name, 
                self.channel_name
            )
            
            await self.accept()

    # Function to disconnet the Socket
    async def disconnect(self, close_code):
        await self.close()
        # pass

    # Custom Notify Function which can be called from Views or api to send message to the frontend
    async def notify(self, event):
        print("Notification sent")
        await self.send(text_data=json.dumps(event["text"]))
