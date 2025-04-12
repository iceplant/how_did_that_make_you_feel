# from django.db import models
# from django.conf import settings
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from .roberta import compute_hugging_face_roberta_emotions
# from textblob import TextBlob
# from django.contrib.auth.base_user import BaseUserManager
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import json
import requests


def compute_hugging_face_roberta_emotions_with_microservice(text):
    """
    Calls the emotion analysis API and returns the response.

    :param text: The text to analyze.
    :return: The JSON response or an error message.
    """
    url = "http://127.0.0.1:8001/emotion"
    headers = {"Content-Type": "application/json"}
    payload = {"text": text}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()  # Raise an error for HTTP 4xx/5xx responses
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def compute_hugging_face_roberta_emotions_with_microservice2(text):
	# EMOTION_API_URL is defined in settings.py This is specific to the microservice
  url =  ("http://127.0.0.1:8001/emotion")
  headers = {"Content-Type": "application/json"}
  data = json.dumps({"text": text})

  try:
      response = requests.post(url, headers=headers, data=data, timeout=5)
      response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
      return response.json()
  except requests.exceptions.RequestException as e:
      return {"error": f"Request failed: {str(e)}"}
  
emotions_json = [[{'label': 'admiration', 'score': 0.00013921984646003693}, {'label': 'amusement', 'score': 0.0002979402197524905}, {'label': 'anger', 'score': 1.1526259186211973e-05}, {'label': 'annoyance', 'score': 4.769671068061143e-05}, {'label': 'approval', 'score': 0.0004311582015361637}, {'label': 'caring', 'score': 2.9983641070430167e-05}, {'label': 'confusion', 'score': 0.00012729559966828674}, {'label': 'curiosity', 'score': 4.310057920520194e-05}, {'label': 'desire', 'score': 0.00013570151349995285}, {'label': 'disappointment', 'score': 5.04086674482096e-05}, {'label': 'disapproval', 'score': 5.802838131785393e-05}, {'label': 'disgust', 'score': 2.0718993255286478e-05}, {'label': 'embarrassment', 'score': 1.0065296919492539e-05}, {'label': 'excitement', 'score': 6.67495041852817e-05}, {'label': 'fear', 'score': 1.9772462110267952e-05}, {'label': 'gratitude', 'score': 2.599145045678597e-05}, {'label': 'grief', 'score': 1.0339751497667748e-05}, {'label': 'joy', 'score': 3.526560612954199e-05}, {'label': 'love', 'score': 8.73627868713811e-06}, {'label': 'nervousness', 'score': 2.7082978704129346e-05}, {'label': 'optimism', 'score': 0.00014460470993071795}, {'label': 'pride', 'score': 1.8028717022389174e-05}, {'label': 'realization', 'score': 0.0001307459024246782}, {'label': 'relief', 'score': 9.67559390119277e-06}, {'label': 'remorse', 'score': 3.393223596503958e-05}, {'label': 'sadness', 'score': 4.196017835056409e-05}, {'label': 'surprise', 'score': 3.807921166298911e-05}, {'label': 'neutral', 'score': 0.9979861974716187}]]
microservices_json =  {'emotions': [[{'label': 'admiration', 'score': 0.00013922010839451104}, {'label': 'amusement', 'score': 0.0002979413256980479}, {'label': 'anger', 'score': 1.1526302841957659e-05}, {'label': 'annoyance', 'score': 4.769680163008161e-05}, {'label': 'approval', 'score': 0.00043115732842125}, {'label': 'caring', 'score': 2.9983757485751994e-05}, {'label': 'confusion', 'score': 0.00012729618174489588}, {'label': 'curiosity', 'score': 4.310057920520194e-05}, {'label': 'desire', 'score': 0.00013570162991527468}, {'label': 'disappointment', 'score': 5.0408911192789674e-05}, {'label': 'disapproval', 'score': 5.802849045721814e-05}, {'label': 'disgust', 'score': 2.0719073290820234e-05}, {'label': 'embarrassment', 'score': 1.006535421765875e-05}, {'label': 'excitement', 'score': 6.674969336017966e-05}, {'label': 'fear', 'score': 1.9772556697716936e-05}, {'label': 'gratitude', 'score': 2.5991550501203164e-05}, {'label': 'grief', 'score': 1.0339790605939925e-05}, {'label': 'joy', 'score': 3.526570799294859e-05}, {'label': 'love', 'score': 8.73630415298976e-06}, {'label': 'nervousness', 'score': 2.7083107852376997e-05}, {'label': 'optimism', 'score': 0.00014460511738434434}, {'label': 'pride', 'score': 1.8028786143986508e-05}, {'label': 'realization', 'score': 0.00013074626622255892}, {'label': 'relief', 'score': 9.675622095528524e-06}, {'label': 'remorse', 'score': 3.39323996740859e-05}, {'label': 'sadness', 'score': 4.196034205961041e-05}, {'label': 'surprise', 'score': 3.8079357182141393e-05}, {'label': 'neutral', 'score': 0.9979861974716187}]]}

if __name__ == "__main__":
  print(compute_hugging_face_roberta_emotions_with_microservice("I am so happy today!"))
  print(compute_hugging_face_roberta_emotions_with_microservice("I am so sad today!"))
  print(compute_hugging_face_roberta_emotions_with_microservice("I am so angry today!"))
  print(compute_hugging_face_roberta_emotions_with_microservice("I am so confused today!"))
  print(compute_hugging_face_roberta_emotions_with_microservice("I am so excited today!"))