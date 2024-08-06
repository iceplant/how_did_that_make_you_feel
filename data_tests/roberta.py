import sys
sys.path.append("..")
from backend.my_secrets import *

from pprint import pprint

import torch

from huggingface_hub import login
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline

login(token=HUGGING_FACE_ROBERTA_TOKEN)

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")

emotion = pipeline('sentiment-analysis', 
                    model='arpanghoshal/EmoRoBERTa', return_all_scores=True)


emotion_labels = emotion("Thanks for using it.")
pprint(emotion_labels)

pipe = pipeline("fill-mask", model="mental/mental-roberta-base")

 
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

