from django.db import models
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

# Create your models here.
class Entry(models.Model):
    title=models.CharField(default="", max_length=150)
    description=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # modified at?
    sentiment = models.FloatField(default=0)

    @property
    def sentiment(self):
        print("reached sentiment calculation")
        print("description: ", self.description)
        ss = sid.polarity_scores(self.description)
        print(f"ss is {ss}")
        return ss['compound']

    # @property
    # def emotions(self):
       
    
    # def save(self, *args, **kwargs):
    #     # Automatically set the selling_price before saving
    #     super().save(*args, **kwargs)


    def __str__(self):
    
      #it will return the title
      return self.title