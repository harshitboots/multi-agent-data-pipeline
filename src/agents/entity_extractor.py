import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an entity extraction agent.
Your job is to identify and extract named entities from documents: people, organisations, locations, dates, amounts, and emails.
You must respond ONLY with valid JSON. No explanation, no markdown, no code fences.
JSON format:
{
    "people": ["John Doe", "Jane Smith"],
    "organisations": ["Acme Corp", "Tech Ltd"],
    "locations": ["New York", "London"],
    "dates": ["2024-01-15", "Q1 2024"],
    "amounts": ["$1,000,000", "50%"],
    "emails": ["john@example.com"],
    "total_entities": 15
}"""

class EntityExtractorResult(BaseModel):
    people: List[str] = Field(default_factory=list)
    organisations: List[str] = Field(default_factory=list)
    locations: List[str] = Field(default_factory=list)
    dates: List[str] = Field(default_factory=list)
    amounts: List[str] = Field(default_factory=list)
    emails: List[str] = Field(default_factory=list)
    total_entities: int = 0

def run(text_preview: str, total_pages: int) -> EntityExtractorResult:
    print("[Entity Extractor Agent] Starting...")

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Extract entities from this document ({total_pages} pages):\n\n{text_preview}"
            }
        ]
    )

    raw = response.content[0].text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        data = json.loads(raw)
        result = EntityExtractorResult(**data)
        print(f"[Entity Extractor Agent] Done — {result.total_entities} entities found")
        return result
    except Exception as e:
        print(f"[Entity Extractor Agent] Error: {e}")
        return EntityExtractorResult()
