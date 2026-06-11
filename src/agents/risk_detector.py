import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a document risk detection agent.
Your job is to identify risks, sensitive data, PII, compliance issues and red flags in documents.
You must respond ONLY with valid JSON. No explanation, no markdown, no code fences.
JSON format:
{
    "pii_detected": true,
    "pii_types": ["names", "emails", "phone numbers"],
    "compliance_risks": ["GDPR risk - personal data present", "risk2"],
    "legal_risks": ["unsigned contract clause", "risk2"],
    "financial_risks": ["large payment terms", "risk2"],
    "overall_risk_score": 7.5,
    "risk_level": "high",
    "recommendations": ["recommendation1", "recommendation2"]
}"""

class RiskDetectorResult(BaseModel):
    pii_detected: bool = False
    pii_types: List[str] = Field(default_factory=list)
    compliance_risks: List[str] = Field(default_factory=list)
    legal_risks: List[str] = Field(default_factory=list)
    financial_risks: List[str] = Field(default_factory=list)
    overall_risk_score: float = 0.0
    risk_level: str = "low"
    recommendations: List[str] = Field(default_factory=list)

def run(text_preview: str, total_pages: int) -> RiskDetectorResult:
    print("[Risk Detector Agent] Starting...")

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Detect risks in this document ({total_pages} pages):\n\n{text_preview}"
            }
        ]
    )

    raw = response.content[0].text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        data = json.loads(raw)
        result = RiskDetectorResult(**data)
        print(f"[Risk Detector Agent] Done — risk level: {result.risk_level}, score: {result.overall_risk_score}/10")
        return result
    except Exception as e:
        print(f"[Risk Detector Agent] Error: {e}")
        return RiskDetectorResult(recommendations=["Could not parse response"])
