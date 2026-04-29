from fastapi import FastAPI
import joblib
import pandas as pd
import uvicorn
from contextlib import asynccontextmanager
from model import match_requests_priority

# قاموس لتخزين النموذج والبيانات بشكل آمن
ml_assets = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # تحميل الأصول عند بدء التشغيل
    try:
        ml_assets["model"] = joblib.load("model.pkl")
        ml_assets["requests_df"] = pd.read_csv("requests.csv")
        print("✅ تم تحميل النموذج والبيانات بنجاح!")
    except Exception as e:
        print(f"❌ خطأ في التحميل: {e}")
    yield
    # تنظيف الذاكرة عند الإغلاق
    ml_assets.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"message": "Matching API is running 🚀"}

@app.post("/match")
def match(payload: dict):
    model = ml_assets.get("model")
    requests_df = ml_assets.get("requests_df")
    
    if model is None or requests_df is None:
        return {"error": "Application assets not loaded properly."}

    donor = payload["donor"]
    results = match_requests_priority(model, requests_df, donor)

    return {"matches": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)