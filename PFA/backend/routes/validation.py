from flask import Blueprint, jsonify, request
from services.generator import generator

validation_bp = Blueprint('validation', __name__)

@validation_bp.route('/validate_answer', methods=['POST'])
def validate_answer():
    data = request.get_json()
    question = data.get('question', {})
    user_answer = data.get('user_answer', '')
    
    if not question or not user_answer:
        return jsonify({"error": "Missing question or answer"}), 400
    
    try:
        prompt = f"""
        Evaluate if this answer is correct for the given question.
        Question: {question.get('question', '')}
        Correct Answer: {question.get('answer', '')}
        User Answer: {user_answer}
        
        Return JSON with:
        - is_correct (boolean)
        - score (0-1)
        - feedback (string)
        - explanation (from question if correct)
        
        Example Response:
        {{
            "is_correct": true,
            "score": 0.9,
            "feedback": "Good answer covering the main points",
            "explanation": "{question.get('explication', '') if question else ''}"
        }}
        """
        
        response = generator.generation_model.generate_content(prompt)
        validation = generator._parse_json(response.text)
        
        validation.setdefault("is_correct", False)
        validation.setdefault("score", 0)
        validation.setdefault("feedback", "Evaluation failed")
        validation.setdefault("explanation", question.get('explication', ''))
        
        return jsonify(validation)
        
    except Exception as e:
        print(f"Validation error: {e}")
        return jsonify({
            "is_correct": False,
            "score": 0,
            "feedback": "Error during evaluation",
            "explanation": question.get('explication', '')
        }), 500