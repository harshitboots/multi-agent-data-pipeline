import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an action item extraction agent.
Your job is to extract all action items, decisions, deadlines, and follow-ups from document text.
You must respond ONLY with valid JSON. No explanation, no markdown, no code fences.
JSON format:
{
    "action_items": ["action1", "action2"],
    "decisions_made": ["decision1", "decision2"],
    "deadlines": ["deadline1 - date", "deadline2 - date"],
    "follow_ups": ["follow up1", "follow up2"],
    "owners": ["person/team responsible1", "person/team responsible2"],
    "priority_actions": ["most urgent action1", "most urgent action2"],
    "total_actions": 8
}"""

class ActionExtractorResult(BaseModel):
    action_items: List[str] = Field(default_factory=list)
    decisions_made: List[str] = Field(default_factory=list)
    deadlines: List[str] = Field(default_factory=list)
    follow_ups: List[str] = Field(default_factory=list)
    owners: List[str] = Field(default_factory=list)
    priority_actions: List[str] = Field(default_factory=list)
    total_actions: int = 0

def run(text_preview: str, total_pages: int) -> ActionExtractorResult:
    print("[Action Extractor Agent] Starting...")

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Extract all action items from this document ({total_pages} pages):\n\n{text_preview}"
            }
        ]
    )

    raw = response.content[0].text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        data = json.loads(raw)
        result = ActionExtractorResult(**data)
        print(f"[Action Extractor Agent] Done — {result.total_actions} actions found")
        return result
    except Exception as e:
        print(f"[Action Extractor Agent] Error: {e}")
        return ActionExtractorResult(action_items=["Could not parse response"])
