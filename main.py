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

def construct_system_prompt() -> str:
    return """
You are an expert in loyalty program business case development and financial analysis.
Create a comprehensive business case for a loyalty program, including financial projections and ROI analysis.

Consider:
1. Initial investment requirements
2. Operational costs
3. Revenue projections and ROI
4. Market analysis and competition
5. Risk factors and mitigation strategies

Provide your response in two parts:
1. A detailed business case narrative including:
   - Executive summary
   - Market opportunity
   - Financial analysis
   - Implementation considerations
   - Risk assessment

2. A structured JSON object with this schema:
{
    "business_case": {
        "executive_summary": "string",
        "investment_required": float,
        "payback_period": "string",
        "five_year_projections": [
            {
                "year": int,
                "revenue": float,
                "costs": float,
                "profit": float,
                "roi": float
            }
        ],
        "key_assumptions": ["assumption1", "assumption2"],
        "risk_factors": ["risk1", "risk2"],
        "success_metrics": ["metric1", "metric2"]
    }
}

Separate the two parts with [JSON_START] and [JSON_END] markers.
"""

def construct_user_prompt(
    company_name: str,
    customer_analysis: Optional[str] = None,
    market_research: Optional[str] = None,
    existing_output: Optional[str] = None,
    feedback: Optional[str] = None
) -> str:
    prompt = f"Create a business case for {company_name}'s loyalty program."
    
    if customer_analysis:
        prompt += f"\n\nCustomer Analysis:\n{customer_analysis}"
    
    if market_research:
        prompt += f"\n\nMarket Research:\n{market_research}"
    
    if existing_output and feedback:
        prompt += f"""
\n\nPrevious Business Case:\n{existing_output}
\nPlease refine based on this feedback:\n{feedback}
"""
    
    return prompt

def extract_json_from_text(text: str) -> dict:
    try:
        start_marker = "[JSON_START]"
        end_marker = "[JSON_END]"
        json_str = text[text.find(start_marker) + len(start_marker):text.find(end_marker)].strip()
        return json.loads(json_str)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse structured data from response: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)