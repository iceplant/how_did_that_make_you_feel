from django.db import models
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from .roberta import compute_hugging_face_roberta_emotions
from textblob import TextBlob
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import requests

from computedfields.models import ComputedFieldsModel
from computedfields.models import ComputedFieldsModel, computed, compute

def compute_hugging_face_roberta_emotions_with_microservice(text):
    url = "http://127.0.0.1:8001/emotion"
    headers = {"Content-Type": "application/json"}
    payload = {"text": text}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()  # Raise an error for HTTP 4xx/5xx responses
        return response.json()['emotions']
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

sid = SentimentIntensityAnalyzer()

# Create your models here.
class Entry(ComputedFieldsModel):
    title=models.CharField(default="", max_length=150)
    description=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # modified at?
    user = models.ForeignKey('AppUser', on_delete=models.CASCADE, related_name='entries')  # Add this line
		
    # Denormalized computed fields
    sentiment = models.FloatField(default=0)
    emotions = models.JSONField(default=dict)
    blob_sentiment = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        if self.pk:
            original = Entry.objects.get(pk=self.pk)
            description_changed = original.description != self.description
        else:
            description_changed = True  # New instance

        if description_changed:
            self.sentiment = sid.polarity_scores(self.description)['compound']
            self.emotions = compute_hugging_face_roberta_emotions_with_microservice(self.description)
            self.blob_sentiment = TextBlob(self.description).sentiment._asdict()
            # self.polarity = blob.polarity
            # self.subjectivity = blob.subjectivity

        super().save(*args, **kwargs)

    def __str__(self):
      #it will return the title
      return self.title

class AppUserManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		email = self.normalize_email(email)
		user = self.model(email=email)
		user.set_password(password)
		user.save()
		return user
	def create_superuser(self, email, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		user = self.create_user(email, password)
		user.is_superuser = True
		user.save()
		return user  

class AppUser(AbstractBaseUser, PermissionsMixin):
	user_id = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=50, unique=True)
	username = models.CharField(max_length=50)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
	objects = AppUserManager()
	def __str__(self):
		return self.username