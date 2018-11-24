from rest_framework import serializers
from .models import UserModel

class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['name', 'email_address', 'age', 'created_on']
        #fields = '__all__'
