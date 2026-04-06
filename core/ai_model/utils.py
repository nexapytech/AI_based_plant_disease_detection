def parse_label(label: str):
    """
    Extract plant name and disease from model label
    """

    label = label.lower()

    if "cassava" in label:
        plant = "cassava"
    elif "tomato" in label:
        plant = "tomato"
    else:
        plant = "unknown"

    # remove plant name from disease text
    disease = label.replace("cassava", "").replace("tomato", "")
    disease = disease.replace("_", " ").strip().title()

    if disease == "" or "healthy" in disease.lower():
        disease = "Healthy"

    return plant, disease