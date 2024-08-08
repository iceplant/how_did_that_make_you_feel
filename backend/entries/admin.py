from django.contrib import admin

from .models import Entry


# Register your models here.
class EntryAdmin(admin.ModelAdmin):
 
    # add the fields of the model here
    list_display = ("title","description","created_at", "sentiment", "emotions", 'blob_sentiment')
 
# we will need to register the
# model class and the Admin model class
# using the register() method
# of admin.site class
admin.site.register(Entry,EntryAdmin)