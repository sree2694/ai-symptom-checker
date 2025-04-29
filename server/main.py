import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import cohere
# Import ML model
from models.ml_model import predict_disease

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Cohere API key
COHERE_API_KEY = os.getenv("COHERE_API_KEY") or "xebIGKYVxWBttc70nPdrJPVNvGrLj5htXur5F6Hq"  # <-- update this
cohere_client = cohere.Client(COHERE_API_KEY)

# FastAPI app
app = FastAPI()

# CORS (allow frontend to talk to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class SymptomRequest(BaseModel):
    age: int
    gender: str
    symptoms: list[str]

class SymptomOnlyRequest(BaseModel):
    symptoms: list[str]

# Route
@app.get("/")
def read_root():
    return {"message": "Welcome to MedAssist AI - Symptom Checker"}

# 1. Cohere (AI) Route
@app.post("/api/check-symptoms")
async def check_symptoms(request: SymptomRequest):
    try:
        logger.info(f"Received input: {request.dict()}")
        
        # Build the prompt
        prompt = f"The user is a {request.age}-year-old {request.gender} experiencing: {', '.join(request.symptoms)}. Suggest possible diseases and treatments."
        logger.info(f"Sending prompt to Cohere: {prompt}")

        # Send to Cohere
        response = cohere_client.generate(
            model='command',  # use 'command' model (it is free/accessible)
            prompt=prompt,
            max_tokens=300,
            temperature=0.7,
        )

        # Extract the AI response correctly
        ai_response = response.generations[0].text.strip()
        logger.info(f"AI Response: {ai_response}")

        return JSONResponse(content={"result": ai_response})

    except cohere.CohereError as e:
        logger.error(f"Cohere API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Cohere API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# 2. Traditional ML (Supervised) Route
@app.post("/api/predict-disease")
async def predict_disease_route(request: SymptomOnlyRequest):
    try:
        logger.info(f"Received symptoms for prediction: {request.dict()}")
        
        # Get the prediction from the model
        prediction = predict_disease(request.symptoms)

        # Check if prediction is invalid (NaN or other invalid values)
        if prediction is None or isinstance(prediction, float) and prediction != prediction:  # Check for NaN
            logger.error("Invalid prediction: NaN returned.")
            raise HTTPException(status_code=500, detail="Invalid prediction: NaN returned.")
        
        logger.info(f"Prediction result: {prediction}")
        return JSONResponse(content={"predicted_disease": prediction})

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
