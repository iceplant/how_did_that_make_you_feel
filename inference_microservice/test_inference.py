import sys
sys.path.append("..")
# from ..my_secrets import HUGGING_FACE_ROBERTA_TOKEN, MENTAL_ROBERTA
# from pprint import pprint
# import torch

import pprint

import os
import sys
sys.path.append("..")
from inference_microservice.my_secrets import *

from huggingface_hub import login
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline

login(token=HUGGING_FACE_ROBERTA_TOKEN)

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")

emotion = pipeline(
   'sentiment-analysis', 
    model='arpanghoshal/EmoRoBERTa', 
    return_all_scores=True
  )


def compute_hugging_face_roberta_emotions(text):
  print("\n\n\nrunning roberta function with: ", text, "\n\n\n")
  if len(text) < 512:
    emotion_labels = emotion(text)
    # pprint(emotion_labels)
    return emotion_labels
  else:
    emotion_labels = emotion(text[:500])
    return emotion_labels
  
if __name__ == "__main__":
    # Example usage
    text = "I am feeling great today!"
    prediction = compute_hugging_face_roberta_emotions(text)
    pprint.pprint(f"Prediction: {prediction}")