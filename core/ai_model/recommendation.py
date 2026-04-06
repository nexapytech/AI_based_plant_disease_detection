"""
Smart recommendation engine for plant leaf diseases.
Supports Cassava, Tomato, Maize, Potato, Apple, Grape, Pepper, Strawberry, etc.
"""

# -----------------------------
# Disease → Plant mapping
# -----------------------------
DISEASE_TO_PLANT = {
    # Cassava
    "cassava bacterial blight": "Cassava",
    "cassava brown streak disease": "Cassava",
    "cassava green mottle": "Cassava",
    "cassava mosaic disease": "Cassava",
    "healthy": "Unknown",

    # Tomato
    "bacterial spot": "Tomato",
    "early blight": "Tomato",
    "late blight": "Tomato",
    "leaf mold": "Tomato",
    "septoria leaf spot": "Tomato",
    "spider mites": "Tomato",
    "target spot": "Tomato",
    "yellow leaf curl virus": "Tomato",
    "mosaic virus": "Tomato",

    # Maize / Corn
    "cercospora leaf spot": "Maize",
    "common rust": "Maize",
    "northern leaf blight": "Maize",

    # Potato
    "early blight": "Potato",
    "late blight": "Potato",

    # Apple
    "scab": "Apple",
    "black rot": "Apple",
    "cedar rust": "Apple",

    # Grape
    "black rot": "Grape",
    "esca": "Grape",
    "leaf blight": "Grape",

    # Pepper
    "bacterial spot": "Pepper",

    # Strawberry
    "leaf scorch": "Strawberry"
}

# -----------------------------
# Recommendations database
# -----------------------------
RECOMMENDATIONS = {
    # Cassava
    "cassava bacterial blight": {
        "advice": [
            "Remove infected leaves",
            "Avoid overhead irrigation",
            "Consult agricultural extension officer"
        ],
        "learn_more": ["https://plantvillage.psu.edu/topics/cassava-bacterial-blight"]
    },
    "cassava brown streak disease": {
        "advice": ["Remove infected plants", "Use resistant varieties"],
        "learn_more": ["https://plantvillage.psu.edu/topics/cassava-brown-streak-disease"]
    },
    "cassava green mottle": {
        "advice": ["Use virus-free cuttings", "Control whitefly vectors"],
        "learn_more": ["https://plantvillage.psu.edu/topics/cassava-green-mottle"]
    },
    "cassava mosaic disease": {
        "advice": ["Plant resistant varieties", "Control whiteflies", "Rogue infected plants"],
        "learn_more": ["https://plantvillage.psu.edu/topics/cassava-mosaic-disease"]
    },

    # Tomato
    "bacterial spot": {
        "advice": ["Remove infected leaves", "Avoid overhead irrigation", "Use copper-based fungicide"],
        "learn_more": ["https://plantvillage.psu.edu/topics/bacterial-spot-tomato"]
    },
    "early blight": {
        "advice": ["Remove infected leaves", "Apply fungicide", "Rotate crops"],
        "learn_more": ["https://plantvillage.psu.edu/topics/early-blight-tomato"]
    },
    "late blight": {
        "advice": ["Use resistant varieties", "Remove infected plants", "Apply fungicides"],
        "learn_more": ["https://plantvillage.psu.edu/topics/late-blight-tomato"]
    },
    "healthy": {
        "advice": ["No action needed, plant is healthy."],
        "learn_more": ["https://plantvillage.psu.edu/"]
    },

    # Maize
    "cercospora leaf spot": {
        "advice": ["Remove infected leaves", "Rotate crops", "Apply fungicide"],
        "learn_more": ["https://plantvillage.psu.edu/topics/cercospora-leaf-spot-maize"]
    },
    "common rust": {
        "advice": ["Remove infected leaves", "Use resistant varieties"],
        "learn_more": ["https://plantvillage.psu.edu/topics/common-rust-maize"]
    },
    "northern leaf blight": {
        "advice": ["Remove infected leaves", "Rotate crops", "Apply fungicides as recommended"],
        "learn_more": ["https://plantvillage.psu.edu/topics/northern-leaf-blight-maize"]
    },

    # Fallback general recommendation
    "unknown": {
        "advice": [
            "Isolate affected plant",
            "Avoid excessive watering",
            "Inspect surrounding plants",
            "Consult agricultural extension officer"
        ],
        "learn_more": [
            "https://plantvillage.psu.edu/",
            "https://www.fao.org/home/en",
            "https://plantwiseplusknowledgebank.org/"
        ]
    }
}

# -----------------------------
# Get recommendation function
# -----------------------------
def get_recommendation(disease_name):
    """
    Returns normalized disease, leaf_name, and recommendations
    """
    disease_key = disease_name.lower().strip().replace("(", "").replace(")", "").replace(" ", "_")
    leaf_name = DISEASE_TO_PLANT.get(disease_name.lower(), "Unknown Plant")
    info = RECOMMENDATIONS.get(disease_name.lower(), RECOMMENDATIONS["unknown"])

    return disease_name, leaf_name, info