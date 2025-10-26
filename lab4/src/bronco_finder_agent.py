import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

import time

class CorrectorAgent:
    def __init__(self, correction_criteria):
        self.correction_criteria = correction_criteria

    def post_process(self, response_text):
        lines = response_text.splitlines()
        start_idx = next((i for i, line in enumerate(lines) if "{" in line), None)
        end_idx = next((i for i, line in reversed(list(enumerate(lines))) if "}" in line), None)
        if start_idx is not None and end_idx is not None and start_idx <= end_idx:
            lines = lines[start_idx:end_idx+1]
        elif not lines:
            lines = []
        return lines
    
    def respond(self, user_input, max_retries=10, delay=10):
        attempt = 1
        while attempt < max_retries:
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=user_input
                )
                
                return self.post_process(response.text)

            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    print(f"Attempt {attempt} failed with 503/UNAVAILABLE. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    if attempt < 10:
                        attempt += 1
                        continue
                else:
                    print(f"An unexpected error occurred: {e}")
                    raise e
            raise RuntimeError(f"All {max_retries} attempts failed due to 503/UNAVAILABLE errors.")
