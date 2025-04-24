# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.openai_helper import get_conditions
import os
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class SymptomRequest(BaseModel):
    age: int
    gender: str
    symptoms: list[str]

@app.post("/api/check-symptoms")
async def check_symptoms(request: SymptomRequest):
    logging.info(f"Input received: {request}")
    result = get_conditions(request.age, request.gender, request.symptoms)
    logging.info(f"AI Response: {result}")
    return result
