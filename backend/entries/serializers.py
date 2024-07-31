# import serializers from the REST framework
from rest_framework import serializers
 
# import the todo data model
from .models import Entry
 
# create a serializer class
class EntrySerializer(serializers.ModelSerializer):
 
    # create a meta class
    class Meta:
        model = Entry
        fields = ('id', 'title', 'description', 'created_at','sentiment', 'emotions')