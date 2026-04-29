from fastapi import FastAPI
import joblib
import pandas as pd
import uvicorn

from model import match_requests_priority

app = FastAPI()

# load model
model = joblib.load("model.pkl")

# load data once 🔥
requests_df = pd.read_csv("requests.csv")

@app.get("/")
def home():
    return {"message": "Matching API is running 🚀"}

@app.post("/match")
def match(payload: dict):
    global model
    global requests_df

    donor = payload["donor"]

    results = match_requests_priority(model, requests_df, donor)

    return {"matches": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)

    