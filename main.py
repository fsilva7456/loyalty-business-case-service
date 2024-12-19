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

def generate_business_case(
    company_name: str,
    customer_analysis: Optional[str] = None,
    market_research: Optional[str] = None,
    existing_output: Optional[str] = None,
    feedback: Optional[str] = None
) -> tuple[str, dict]:
    """Generate business case using OpenAI's API"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": construct_system_prompt()},
                {"role": "user", "content": construct_user_prompt(
                    company_name,
                    customer_analysis,
                    market_research,
                    existing_output,
                    feedback
                )}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        full_response = response.choices[0].message.content
        narrative = full_response[:full_response.find("[JSON_START]")].strip()
        structured_data = extract_json_from_text(full_response)
        
        return narrative, structured_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate", response_model=BusinessCaseResponse)
async def generate_analysis(request: BusinessCaseRequest):
    # Extract data from request
    customer_analysis = None
    market_research = None
    if request.previous_data:
        customer_analysis = request.previous_data.customer_analysis
        market_research = request.previous_data.market_research
    
    existing_output = None
    feedback = None
    if request.current_prompt_data:
        existing_output = request.current_prompt_data.existing_generated_output
        feedback = request.current_prompt_data.user_feedback
    
    # Generate business case
    generated_text, structured_data = generate_business_case(
        request.company_name,
        customer_analysis,
        market_research,
        existing_output,
        feedback
    )
    
    # Prepare response
    return BusinessCaseResponse(
        generated_output=generated_text,
        structured_data=structured_data
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)