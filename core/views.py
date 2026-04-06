import os
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage

from core.ai_model.hf_models import detect_leaf
from core.ai_model.recommendation import get_recommendation

# -----------------------------
# Severity calculator
# -----------------------------
def get_severity(confidence: float) -> str:
    if confidence >= 0.85:
        return "High"
    elif confidence >= 0.6:
        return "Medium"
    return "Low"

# -----------------------------
# API Endpoint
# -----------------------------
import os
import uuid
import logging
from django.core.files.storage import default_storage

from django.core.files.base import ContentFile
import base64
from django.conf import settings
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
logger = logging.getLogger(__name__)


from PIL import Image

import os
import uuid
import base64
import logging
import io 

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response






@csrf_exempt
@api_view(["POST"])
def detect(request):
    """
    Detect leaf disease from Base64 image sent via MIT App Inventor PostText.
    Optional plant name can be sent via query parameter: ?plant=Cassava
    """
    temp_path = None

    try:
        # 1️⃣ Get Base64 from raw POST text
        image_base64 = request.body.decode("utf-8")
        plant_hint = request.GET.get("plant")  # optional

        if not image_base64:
            return Response({"error": "No image provided"}, status=400)

        # 2️⃣ Clean Base64
        image_base64 = image_base64.replace(" ", "").replace("\n", "")
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]

        # Fix padding
        missing_padding = len(image_base64) % 4
        if missing_padding:
            image_base64 += "=" * (4 - missing_padding)

        # 3️⃣ Decode and validate
        try:
            image_bytes = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()  # validate image
        except Exception:
            return Response({"error": "Invalid image data"}, status=400)

        # Reopen image for saving
        image = Image.open(io.BytesIO(image_bytes))

        # 4️⃣ Save to MEDIA_ROOT
        filename = f"leaf_{uuid.uuid4().hex}.jpg"
        media_root = getattr(settings, "MEDIA_ROOT", "media")
        os.makedirs(media_root, exist_ok=True)
        temp_path = os.path.join(media_root, filename)
        image.save(temp_path, format="JPEG")

        logger.info(f"Image saved at {temp_path}")

        # 5️⃣ Run detection
        plant, disease, confidence = detect_leaf(temp_path, plant_hint=plant_hint)
        confidence = round(float(confidence), 4)
        severity = get_severity(confidence)
        normalized_disease, leaf_name, info = get_recommendation(disease)

        # Build optional image URL if MEDIA_URL is set
        image_url = request.build_absolute_uri(
            settings.MEDIA_URL + filename if hasattr(settings, "MEDIA_URL") else filename
        )

        return Response({
            "leaf_name": plant_hint,
            "disease": normalized_disease.replace("_", " ").title(),
            "confidence": confidence,
            "severity": severity,
            "recommendations": info.get("advice", ""),
            "learn_more": info.get("learn_more", ""),
            "image_url": image_url
        })
   

    except Exception as e:
        logger.exception("Error processing leaf detection")
        return Response({"error": str(e)}, status=500)

    finally:
        # Optional cleanup: remove saved image after detection
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
                print(plant_hint, normalized_disease.replace("_", " ").title(), severity)
            except Exception as cleanup_error:
                logger.warning(f"Failed to remove temp file: {cleanup_error}")