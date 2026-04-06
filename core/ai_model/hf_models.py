"""
Unified multi-plant leaf + disease detection
Supports:
- Cassava
- Tomato, Maize, Potato, Apple, Grape, Pepper, Strawberry, Cherry, Peach, Orange
"""

from transformers import pipeline, AutoModelForImageClassification
from torchvision import transforms
from PIL import Image
import torch
import re
from PIL import Image
from decouple import config
CONFIDENCE_THRESHOLD = 0.55

# =====================================================
# Supported plants and their models
# =====================================================
PLANTS = [
    "cassava","tomato","maize","corn","potato","apple",
    "grape","pepper","strawberry","cherry","peach","orange"
]

# =========================
# Cassava model (HF pipeline)
# =========================
CASSAVA_CLASSIFIER = pipeline(
    "image-classification",
    model="nexusbert/resnet50-cassava-finetuned",
  
   
   
)

# =========================
# Mesabo model (Tomato, Maize, Potato, Apple, Grape, Pepper, etc.)
# Manual wrapper
# =========================
MESABO_MODEL_NAME = "mesabo/agri-plant-disease-resnet50"

MESABO_MODEL = AutoModelForImageClassification.from_pretrained(
    MESABO_MODEL_NAME,
  
   
)
MESABO_MODEL.eval()

MESABO_TRANSFORM = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485,0.456,0.406],
        std=[0.229,0.224,0.225]
    )
])

class MesaboPipelineLike:
    """Makes mesabo model behave like HF pipeline"""
    def __call__(self, image_path):
        image = Image.open(image_path).convert("RGB")
        tensor = MESABO_TRANSFORM(image).unsqueeze(0)
        with torch.no_grad():
            outputs = MESABO_MODEL(tensor)
            probs = torch.softmax(outputs.logits, dim=1)

        scores = probs[0].tolist()
        labels = MESABO_MODEL.config.id2label

        results = [{"label": labels[i], "score": scores[i]} for i in range(len(scores))]
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

MESABO_CLASSIFIER = MesaboPipelineLike()

# =========================
# Predict with classifier
# =========================
def predict_with_classifier(image_path, classifier):
    results = classifier(image_path)
    best = results[0]
    label = best["label"]
    confidence = float(best["score"])
    if confidence < CONFIDENCE_THRESHOLD:
        return "unknown_leaf", confidence
    return label, confidence

# =========================
# Parse labels
# =========================
def parse_label(label: str, plant_hint=None):
    label_lower = label.lower()
    plant = "unknown"

    # Determine plant based on hint first
    if plant_hint:
        plant = plant_hint.lower()
    else:
        for p in PLANTS:
            if p in label_lower:
                plant = p
                break

    # Remove plant name from label to get disease
    disease = label_lower
    if plant != "unknown":
        disease = disease.replace(plant.lower(),"")
    disease = re.sub(r"[()]", "", disease)
    disease = disease.replace("_"," ").strip().title()
    if disease == "":
        disease = "Healthy"

    return plant.capitalize(), disease



# =========================
# Detect leaf
# =========================
def detect_leaf(image_path, plant_hint=None):
    """
    Detect leaf + disease using appropriate model:
    - Cassava -> cassava model
    - Others -> mesabo model
    plant_hint: optional string from user input (e.g., "cassava", "tomato")
    """

    if plant_hint and plant_hint.lower() == "cassava":
        # Use Cassava model
        label, confidence = predict_with_classifier(image_path, CASSAVA_CLASSIFIER)
        plant, disease = parse_label(label, plant_hint="cassava")
        return plant, disease, confidence

    # Use Mesabo model for all others
    label, confidence = predict_with_classifier(image_path, MESABO_CLASSIFIER)
    plant, disease = parse_label(label, plant_hint=plant_hint)
    return plant, disease, confidence


