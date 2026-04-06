import os
import requests
from decouple import config

HF_TOKEN = config("HF_TOKEN")  # Hugging Face API token
CONFIDENCE_THRESHOLD = 0.55

# Hugging Face model URLs (replace with your endpoint if deployed)
HF_MODELS = {
    "cassava": "https://api-inference.huggingface.co/models/nexusbert/resnet50-cassava-finetuned",
    "tomato": "https://api-inference.huggingface.co/models/mesabo/agri-plant-disease-resnet50"
}

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/octet-stream"
}

def call_hf_model(image_bytes, plant):
    url = HF_MODELS.get(plant)
    if not url:
        raise ValueError(f"No Hugging Face model defined for plant: {plant}")
    response = requests.post(url, headers=HEADERS, data=image_bytes)
    response.raise_for_status()
    results = response.json()
    if not results:
        return "unknown_leaf", 0.0
    best = results[0]
    label = best.get("label", "unknown_leaf")
    confidence = float(best.get("score", 0.0))
    if confidence < CONFIDENCE_THRESHOLD:
        return "unknown_leaf", confidence
    return label, confidence