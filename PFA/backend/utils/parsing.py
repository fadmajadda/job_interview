import json
import re
from typing import Dict

def parse_json(text: str) -> Dict:
    try:
        text = re.sub(r'```json|```', '', text).strip()
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON: {e}")
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != -1:
                return json.loads(text[start:end])
        except Exception:
            pass
        
        print(f"Contenu problématique: {text}")
        return {
            "language": "fr",
            "languages": [],
            "frameworks": [],
            "tools": [],
            "concepts": [],
            "level": "mid",
            "soft_skills": []
        }