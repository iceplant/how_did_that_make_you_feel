from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
from huggingface_hub import login
import logging

# import torch

import sys
sys.path.append("..")
from inference_microservice.my_secrets import *

# Initialize FastAPI app
app = FastAPI()

# Hugging Face authentication (replace with your token)
login(token=HUGGING_FACE_ROBERTA_TOKEN)

# Load EmoRoBERTa model and tokenizer (PyTorch version)
emotion_tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
# emotion_model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")
# emotion_pipeline = pipeline(
#     "sentiment-analysis", 
#     model=emotion_model, 
#     tokenizer=emotion_tokenizer, 
#     framework="tf",
#     return_all_scores=True
#   )

emotion = pipeline(
   'sentiment-analysis', 
    model='arpanghoshal/EmoRoBERTa', 
    framework="tf",
    return_all_scores=True
  )

# Load Mental-RoBERTa model and tokenizer
# mask_pipeline = pipeline("fill-mask", model="mental/mental-roberta-base")

# Request and response schemas
class EmotionRequest(BaseModel):
    text: str

class EmotionResponse(BaseModel):
    emotions: list

class FillMaskRequest(BaseModel):
    text: str

class FillMaskResponse(BaseModel):
    predictions: list

# Endpoint for emotion analysis
@app.post("/emotion", response_model=EmotionResponse)
async def analyze_emotion(request: EmotionRequest):
    try:
        # Perform emotion analysis
        emotions = emotion(request.text)
        return {"emotions": emotions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# # Endpoint for fill-mask prediction
# @app.post("/fill-mask", response_model=FillMaskResponse)
# async def fill_mask(request: FillMaskRequest):
#     try:
#         # Perform fill-mask prediction
#         predictions = mask_pipeline(request.text)
#         return {"predictions": predictions}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))