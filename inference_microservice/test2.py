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
  
if __name__ == "__main__":
  print(compute_hugging_face_roberta_emotions_with_microservice("I am so happy today!"))
  print(compute_hugging_face_roberta_emotions_with_microservice("I am so sad today!"))
  print(compute_hugging_face_roberta_emotions_with_microservice("I am so angry today!"))
  print(compute_hugging_face_roberta_emotions_with_microservice("I am so confused today!"))
  print(compute_hugging_face_roberta_emotions_with_microservice("I am so excited today!"))