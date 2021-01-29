from channels.generic.websocket import AsyncWebsocketConsumer

import json

class NotificationConsumer(AsyncWebsocketConsumer):
    
    # Function to connect to the websocket
    async def connect(self):
       # Checking if the User is logged in

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

class OrderStatusConsumer(AsyncWebsocketConsumer):

    # Function to connect to the websocket
    async def connect(self):
       # Checking if the User is logged in

            # print(self.scope["user"])   # Can access logged in user details by using self.scope.user, Can only be used if AuthMiddlewareStack is used in the routing.py
            # self.group_name = str(self.scope["user"].pk)  # Setting the group name as the pk of the user primary key as it is unique to each user. The group name is used to communicate with the user.
        self.group_name = "Order_Status_Group"  # Setting the group name as the pk of the user primary key as it is unique to each user. The group name is used to communicate with the user.
        
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
    async def update_status(self, event):
        print("Order status updated")
        await self.send(text_data=event["text"])
