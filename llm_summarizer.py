from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """You are a clinical documentation assistant. You will be given a doctor's free-text visit note. 
Extract the information into strict JSON with exactly these fields:
- "symptoms": a short list of symptoms mentioned (array of strings)
- "probable_diagnosis": a brief phrase, prefixed with "AI-suggested (not a diagnosis):"
- "follow_up_plan": a short summary of any follow-up mentioned
- "flags": any urgent or concerning items mentioned, or "None" if nothing urgent

Respond with ONLY the JSON object, no other text, no markdown code fences.

Example input: "Patient reports chest pain and shortness of breath for 2 days. ECG ordered. Advised to return immediately if symptoms worsen."
Example output:
{"symptoms": ["chest pain", "shortness of breath"], "probable_diagnosis": "AI-suggested (not a diagnosis): possible cardiac concern", "follow_up_plan": "ECG ordered", "flags": "Advised immediate return if symptoms worsen"}
"""


def summarize_note(raw_note: str) -> dict:
    """
    Sends a free-text clinical note to the LLM and returns a structured summary.
    This is a documentation aid only — not a diagnostic tool.
    """
    if not raw_note or not raw_note.strip():
        return {
            "symptoms": [],
            "probable_diagnosis": "No note provided",
            "follow_up_plan": "N/A",
            "flags": "None"
        }

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\nNote to summarize:\n{raw_note}"
        )
        text = response.text.strip()
        # Strip markdown code fences if the model adds them despite instructions
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "symptoms": ["Error: could not parse AI response"],
            "probable_diagnosis": "N/A",
            "follow_up_plan": "N/A",
            "flags": "Parsing error — please review note manually"
        }
    except Exception as e:
        return {
            "symptoms": [f"Error calling AI service: {str(e)}"],
            "probable_diagnosis": "N/A",
            "follow_up_plan": "N/A",
            "flags": "Service error — please review note manually"
        }

if __name__ == "__main__":
    pass  # test code removed — now called from app.py  