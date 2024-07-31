from django.db import models
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

# Create your models here.
class Entry(models.Model):
    title=models.CharField(max_length=150)
    description=models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    # modified at?
    sentiment = models.FloatField(default=0)

    @property
    def calculate_sentiment(self):
        ss = sid.polarity_scores(self.description)
        return ss['compound']


    def __str__(self):
    
      #it will return the title
      return self.title