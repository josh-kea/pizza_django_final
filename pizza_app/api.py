from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from .models import Pizza

from .serializers import PizzaSerializer
from .permissions import IsEmployeeOrNoAccess



class PizzaList(generics.ListCreateAPIView):
   permission_classes = [IsEmployeeOrNoAccess]
   queryset = Pizza.objects.all()
   serializer_class = PizzaSerializer
   
class PizzaDetail(generics.RetrieveUpdateDestroyAPIView):
   permission_classes = [IsEmployeeOrNoAccess]
   queryset = Pizza.objects.all()
   serializer_class = PizzaSerializer