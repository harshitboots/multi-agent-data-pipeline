import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a document parsing agent.
Your job is to analyse extracted PDF text and identify document structure, metadata and content type.
You must respond ONLY with valid JSON. No explanation, no markdown, no code fences.
JSON format:
{
    "document_type": "invoice/contract/report/letter/other",
    "language": "English",
    "total_sections": 5,
    "has_tables": true,
    "has_numbers": true,
    "key_topics": ["topic1", "topic2", "topic3"],
    "document_quality": "good/fair/poor",
    "parsing_notes": ["note1", "note2"]
}"""

class PDFParserResult(BaseModel):
    document_type: str = "unknown"
    language: str = "English"
    total_sections: int = 0
    has_tables: bool = False
    has_numbers: bool = False
    key_topics: List[str] = Field(default_factory=list)
    document_quality: str = "unknown"
    parsing_notes: List[str] = Field(default_factory=list)

def run(text_preview: str, total_pages: int) -> PDFParserResult:
    print("[PDF Parser Agent] Starting...")

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Parse this PDF document ({total_pages} pages):\n\n{text_preview}"
            }
        ]
    )

    raw = response.content[0].text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        data = json.loads(raw)
        result = PDFParserResult(**data)
        print(f"[PDF Parser Agent] Done — {result.document_type} document detected")
        return result
    except Exception as e:
        print(f"[PDF Parser Agent] Error: {e}")
        return PDFParserResult(parsing_notes=["Could not parse response"])
