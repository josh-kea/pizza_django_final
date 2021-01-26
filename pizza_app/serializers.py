from rest_framework import serializers
from .models import Pizza

class PizzaSerializer(serializers.ModelSerializer):
   class Meta:
      fields = '__all__' # all model fields will be included
      model = Pizza