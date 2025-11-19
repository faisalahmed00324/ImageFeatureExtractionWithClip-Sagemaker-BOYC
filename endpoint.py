# app.py
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
from io import BytesIO
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import uvicorn

app = FastAPI(title="CLIP API")
print("Starting up...")
# Load CLIP once at startup
model_name = "/opt/program/model"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)
model.eval()

class ImageRequest(BaseModel):
    image: str  # base64 encoded

class TextRequest(BaseModel):
    text: str

@app.get("/ping")
def ping():
    return {"status": "Healthy"}

@app.post("/invocations")
def get_embedding(req: ImageRequest):
    try:
        image_bytes = base64.b64decode(req.image)
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            embedding = model.get_image_features(**inputs)
        embedding = embedding / embedding.norm(p=2, dim=-1, keepdim=True)
        return {"embedding": embedding.squeeze().tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/text-embedding")
def get_text_embedding(req: TextRequest):
    try:
        inputs = processor(text=req.text, return_tensors="pt", padding=True)
        with torch.no_grad():
            embedding = model.get_text_features(**inputs)
        embedding = embedding / embedding.norm(p=2, dim=-1, keepdim=True)
        return {"embedding": embedding.squeeze().tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    # SageMaker invokes with "serve" argument
    if "serve" in sys.argv:
        uvicorn.run(app, host="0.0.0.0", port=8080)