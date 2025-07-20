from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Feature(BaseModel):
    title: str
    description: str

@app.get("/")
def read_root():
    return {"message": "Welcome to Dejavas API"}

@app.post("/submit-features/")
def submit_features(features: List[Feature]):
    return {
        "received_count": len(features),
        "features": features
    }
