import os, io, base64

from datetime import datetime

from fastapi import FastAPI, File, UploadFile, Body, Depends
from pydantic import BaseModel
from segment_anything import build_sam, SamPredictor

from PIL import Image



from fastapi.middleware.cors import CORSMiddleware

from huggingface_hub import hf_hub_download

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schemas

class UploadRequest(BaseModel):
    file: str


@app.get("/")
def read_root():
    return {"Hello": "World"}

# Get image from b64

def get_model_path() -> str:

    result = hf_hub_download("ybelkada/segment-anything", "checkpoints/sam_vit_b_01ec64.pth")

    return result

@app.post('/upload-image/')
async def upload_image(body: UploadRequest = Body(...), model_path = Depends(get_model_path)):

    # # Load the model
    predictor = SamPredictor(build_sam(checkpoint=model_path))

    # Load the image
    img = body.file

    # clean base64 string
    img = img.replace('data:image/png;base64,', '')

    # Load and save the image
    img = Image.open(io.BytesIO(base64.b64decode(img)))

    filename = f'{datetime.timestamp(datetime.now())}.png'
    path = f'{BASE_DIR}/app/uploads/{filename}'

    img.save(path, format="PNG", quality=100)

    # # Set image

    predictor.set_image(img)

    # Predict
    masks, _, _ = predictor.predict('astronaut')

    print(masks)

    return { 'result': 'ok'}
    

