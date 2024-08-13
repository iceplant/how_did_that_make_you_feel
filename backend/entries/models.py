from django.db import models
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from .roberta import compute_hugging_face_roberta_emotions
from textblob import TextBlob
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


sid = SentimentIntensityAnalyzer()

# Create your models here.
class Entry(models.Model):
    title=models.CharField(default="", max_length=150)
    description=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # modified at?
    sentiment = models.FloatField(default=0)
    emotions = models.JSONField()
    blob_sentiment = models.JSONField()

    @property
    def sentiment(self):
        # print("reached sentiment calculation")
        # print("description: ", self.description)
        ss = sid.polarity_scores(self.description)
        # print(f"ss is {ss}")
        return ss['compound']

    @property
    def emotions(self):
      emotions_json = compute_hugging_face_roberta_emotions(self.description)
      return emotions_json
    
    @property
    def blob_sentiment(self):
      #  return {"polarity" : "Your mom", "subjectivity" : "your dad"}
      return TextBlob(self.description).sentiment


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