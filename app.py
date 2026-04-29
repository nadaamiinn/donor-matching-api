from fastapi import FastAPI
import joblib
import pandas as pd
import uvicorn


from model import match_requests_priority

app = FastAPI()

# load model
model = joblib.load("model.pkl")


@app.get("/")
def home():
    return {"message": "Matching API is running 🚀"}


@app.post("/match")
def match(payload: dict):

    donor = payload["donor"]
    requests_df = pd.read_csv("requests.csv")
    results = match_requests_priority(model, requests_df, donor)


    return {
        "matches": results
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)