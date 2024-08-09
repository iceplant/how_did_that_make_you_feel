import sys
sys.path.append("..")
# from ..my_secrets import HUGGING_FACE_ROBERTA_TOKEN, MENTAL_ROBERTA
# from pprint import pprint
# import torch

import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 
MENTAL_ROBERTA = os.getenv("MENTAL_ROBERTA")
HUGGING_FACE_ROBERTA_TOKEN = os.getenv("HUGGING_FACE_ROBERTA_TOKEN")

from huggingface_hub import login
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline

login(token=HUGGING_FACE_ROBERTA_TOKEN)

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")

emotion = pipeline('sentiment-analysis', 
                        model='arpanghoshal/EmoRoBERTa', return_all_scores=True)


def compute_hugging_face_roberta_emotions(text):
  print("\n\n\nrunning roberta function with: ", text, "\n\n\n")
  if len(text) < 512:
    emotion_labels = emotion(text)
    # pprint(emotion_labels)
    return emotion_labels
  else:
    emotion_labels = emotion(text[:500])
    return emotion_labels

# pipe = pipeline("fill-mask", model="mental/mental-roberta-base")

 
##################################################

# from transformers import AutoTokenizer, AutoModel

# login(token=MENTAL_ROBERTA)

# tokenizer = AutoTokenizer.from_pretrained("mental/mental-roberta-base")
# model = AutoModel.from_pretrained("mental/mental-roberta-base")
# def predict(text):
#     # Tokenize the input text
#     inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    
#     # Perform inference
#     with torch.no_grad():
#         outputs = model(**inputs)

#     return outputs 
#     # # Extract logits and make predictions
#     # logits = outputs.logits
#     # predictions = torch.argmax(logits, dim=1)
    
#     # return predictions.item()

# # Example usage
# text = "I am feeling great today!"
# prediction = predict(text)
# print(f"Prediction: {prediction}")

