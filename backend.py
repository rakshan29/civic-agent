import os
import logging
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("CivicBackend")

# Initialize Gemini Client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.warning("GEMINI_API_KEY is missing! Make sure to set it in .env")

client = genai.Client(api_key=api_key)

# Define structured Pydantic Schema
class ClassifiedAction(BaseModel):
    category: str = Field(description="Infrastructure, Sanitation, Public Health, or Emergency")
    urgency_level: str = Field(description="CRITICAL, HIGH, MEDIUM, LOW")
    department_webhook: str = Field(description="Target department slug e.g. public-works-dept")
    extracted_entities: List[str] = Field(description="Key locations or hazard details extracted")
    community_response: str = Field(description="Empathic response message for the citizen")

def triage_citizen_issue(issue_description: str, location: str = "Unspecified") -> ClassifiedAction:
    """Uses Gemini 2.5 Flash to triage citizen issues into structured data."""
    system_instruction = (
        "You are a Dispatch Agent for local communities. "
        "Analyze citizen issues and extract key details into the requested JSON schema."
    )

    prompt = f"Issue: {issue_description}\nLocation: {location}"

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
            response_mime_type="application/json",
            response_schema=ClassifiedAction,
        ),
    )

    return ClassifiedAction.model_validate_json(response.text)

if __name__ == "__main__":
    test_result = triage_citizen_issue("There is a severe water pipeline leak on Main Street overflowing near the school.", "Ward 4")
    print("\n--- Backend Test Output ---")
    print(test_result.model_dump_json(indent=2))
