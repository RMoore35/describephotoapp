from dotenv import load_dotenv
import os
import google.generativeai as genai
import time

load_dotenv()
ACCESS_KEY = os.getenv("geminiKey")

# Configure once (best practice)
genai.configure(api_key=os.getenv("GEMINI_API_KEY", ACCESS_KEY))

# Fast, free-tier-friendly model
MODEL = genai.GenerativeModel(
    "gemini-2.5-flash",
    generation_config={
        "temperature": 0.2,         # Very consistent corrections
        "max_output_tokens": 2048,
    }
)

def fix(text: str) -> str:
    """
    Fixes grammar, spelling, punctuation, and basic style issues.
    Returns ONLY the corrected text (no explanations, no markdown).
    """
    try:
        response = MODEL.generate_content(
            f"Fix all grammar, spelling, punctuation, and style errors. "
            f"Return ONLY the corrected text, nothing else:\n\n{text}"
        )
        return response.text.strip()
    
    except genai.types.generation_types.BlockedError:
        return text  # Safety block → return original
    except Exception as e:
        if "RESOURCE_EXHAUSTED" in str(e):
            print("Rate limit — sleeping 65 seconds...")
            time.sleep(65)
            return fix(text)  # retry once
        print(f"Gemini error: {e}")
        return text
