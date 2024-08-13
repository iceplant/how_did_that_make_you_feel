# import serializers from the REST framework
from xml.dom import ValidationErr
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
 
# import the todo data model
from .models import Entry

UserModel = get_user_model()

 
# create a serializer class
class EntrySerializer(serializers.ModelSerializer):
 
    # create a meta class
    class Meta:
        model = Entry
        fields = ('id', 'title', 'description', 'created_at','sentiment', 'emotions', 'blob_sentiment')

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
      model = UserModel
      fields = '__all__'
    def create(self, clean_data):
        user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'])
        user_obj.username = clean_data['username']
        user_obj.save()
        return user_obj
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        user = authenticate(username=clean_data['email'], password=clean_data['password'])
        if not user:
            raise ValidationErr('user not found')
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: UserModel
        fields = ('email', 'username')