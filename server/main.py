from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.openai_helper import get_conditions
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()
app = FastAPI()

# Allow all frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Request body model
class SymptomRequest(BaseModel):
    age: int
    gender: str
    symptoms: list[str]

# API route
from fastapi import HTTPException

@app.post("/api/check-symptoms")
async def check_symptoms(request: SymptomRequest):
    try:
        logging.info(f"Input received: {request}")
        result = get_conditions(request.age, request.gender, request.symptoms)
        logging.info(f"AI Response: {result}")
        return result
    except Exception as e:
        logging.error(f"Error processing the request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/")
def read_root():
    return {"message": "MedAssist AI backend is running!"}
