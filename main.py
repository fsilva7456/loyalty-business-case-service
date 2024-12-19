import os
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import json

app = FastAPI(title="Loyalty Program Business Case Service")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PreviousData(BaseModel):
    customer_analysis: Optional[str] = None
    market_research: Optional[str] = None

class CurrentPromptData(BaseModel):
    existing_generated_output: str
    user_feedback: str

class BusinessCaseRequest(BaseModel):
    company_name: str
    previous_data: Optional[PreviousData] = None
    current_prompt_data: Optional[CurrentPromptData] = None
    other_input_data: Optional[Dict] = {}

class FinancialProjection(BaseModel):
    year: int
    revenue: float
    costs: float
    profit: float
    roi: float

class BusinessCaseResponse(BaseModel):
    generated_output: str
    structured_data: Dict

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)