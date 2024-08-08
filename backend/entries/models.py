from django.db import models
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from .roberta import compute_hugging_face_roberta_emotions
from textblob import TextBlob


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