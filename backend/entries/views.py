from django.shortcuts import render
 
# import view sets from the REST framework
from rest_framework import viewsets
 
# import the TodoSerializer from the serializer file
from .serializers import EntrySerializer
 
# import the Todo model from the models file
from .models import Entry
 
# create a class for the Todo model viewsets
class EntryView(viewsets.ModelViewSet):
 
    # create a serializer class and 
    # assign it to the TodoSerializer class
    serializer_class = EntrySerializer
 
    # define a variable and populate it 
    # with the Todo list objects
    queryset = Entry.objects.all()