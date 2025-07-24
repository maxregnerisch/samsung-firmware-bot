import os
import requests
import glob
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

SYSTEM_PROMPT = """
You are an expert Samsung developer specializing in OneUI 8 optimizations. Analyze the provided Python code and:
1. Identify OneUI 8 compatibility issues
2. Optimize performance for firmware scraping
3. Improve error handling for Samsung device variations
4. Enhance API interactions
5. Update deprecated libraries
6. Add type hints where beneficial
7. Suggest security improvements

Return ONLY the modified code in a single code block. Include no explanations.
"""

def get_enhanced_code(content):
    prompt = f"```python\n{content}\n```\n\nImprove this Samsung firmware bot code for OneUI 8 compatibility:"
    
    payload = {
        "model": "deepseek-coder",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 4096
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"API Error: {e}")
        return None

def extract_code(response):
    match = re.search(r"```python\n(.*?)\n```", response, re.DOTALL)
    return match.group(1) if match else response

def process_files():
    for filepath in glob.glob("**/*.py", recursive=True):
        if "enhancements" in filepath:
            continue
            
        print(f"Processing: {filepath}")
        
        with open(filepath, "r") as f:
            original = f.read()
        
        enhanced = get_enhanced_code(original)
        if not enhanced:
            continue
        
        clean_code = extract_code(enhanced)
        
        output_dir = os.path.join("enhancements", os.path.dirname(filepath))
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, f"{os.path.basename(filepath)}")
        with open(output_path, "w") as f:
            f.write(clean_code)
        print(f"Generated enhancement: {output_path}")

if __name__ == "__main__":
    print("Starting OneUI 8 optimization...")
    process_files()
    print("Enhancement complete!")
