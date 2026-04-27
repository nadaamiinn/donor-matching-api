from fastapi import FastAPI
import pandas as pd
import joblib

from model import match_requests_priority

app = FastAPI()

# load model
model = joblib.load("Models/model.pkl")


@app.get("/")
def home():
    return {"message": "Matching API is running 🚀"}


@app.post("/match")
def match(payload: dict):

    donor = payload["donor"]
    requests = pd.DataFrame(payload["requests"])

    results = match_requests_priority(model, requests, donor)

    return {
        "matches": results
    }