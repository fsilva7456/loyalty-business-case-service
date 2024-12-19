# Loyalty Program Business Case Service

This FastAPI service generates comprehensive business cases for loyalty programs using OpenAI's GPT-4 model.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/fsilva7456/loyalty-business-case-service.git
   cd loyalty-business-case-service
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'  # On Windows: set OPENAI_API_KEY=your-api-key-here
   ```

## Running the Service

1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

2. The service will be available at `http://localhost:8000`

## API Documentation

### Generate Business Case Endpoint

`POST /generate`

Generates a detailed business case for a loyalty program including financial projections.

Request format:
```json
{
  "company_name": "string",
  "previous_data": {
    "customer_analysis": "string (if available)",
    "market_research": "string (if available)"
  },
  "current_prompt_data": {
    "existing_generated_output": "string",
    "user_feedback": "string"
  },
  "other_input_data": {}
}
```

Response format:
```json
{
  "generated_output": "Detailed business case narrative...",
  "structured_data": {
    "business_case": {
      "executive_summary": "string",
      "investment_required": 100000.0,
      "payback_period": "18 months",
      "five_year_projections": [
        {
          "year": 1,
          "revenue": 250000.0,
          "costs": 150000.0,
          "profit": 100000.0,
          "roi": 0.25
        }
      ],
      "key_assumptions": ["assumption1", "assumption2"],
      "risk_factors": ["risk1", "risk2"],
      "success_metrics": ["metric1", "metric2"]
    }
  }
}
```

## Key Features

- Generates comprehensive business cases using GPT-4
- Incorporates customer analysis and market research
- Provides detailed financial projections
- Supports iterative refinement through feedback
- Includes:
  - Executive summary
  - Investment requirements
  - 5-year financial projections
  - ROI analysis
  - Risk assessment
  - Success metrics

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Interactive API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`