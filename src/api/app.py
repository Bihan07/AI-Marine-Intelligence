from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd


# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load("src/ml/species_model.pkl")


# ==========================================
# CREATE API
# ==========================================

app = FastAPI(
    title="AI Marine Intelligence API",
    description="ML-based marine species prediction",
    version="1.0",
)


# ==========================================
# INPUT FORMAT
# ==========================================


class PredictionRequest(BaseModel):
    latitude: float
    longitude: float
    depth: float
    month: int


# ==========================================
# HOME
# ==========================================


@app.get("/")
def home():

    return {"message": "AI Marine Intelligence API is running"}


# ==========================================
# PREDICTION
# ==========================================


@app.post("/predict")
def predict(request: PredictionRequest):

    # Create input dataframe

    data = pd.DataFrame(
        {
            "decimalLatitude": [request.latitude],
            "decimalLongitude": [request.longitude],
            "depth": [request.depth],
            "month": [request.month],
        }
    )

    # Prediction

    prediction = model.predict(data)[0]

    # Probabilities

    probabilities = model.predict_proba(data)[0]

    classes = model.classes_

    # Create results

    results = []

    for species, probability in zip(classes, probabilities):
        results.append(
            {"species": species, "probability": round(float(probability) * 100, 2)}
        )

    # Sort highest probability first

    results.sort(key=lambda x: x["probability"], reverse=True)

    return {"prediction": prediction, "top_predictions": results[:5]}
