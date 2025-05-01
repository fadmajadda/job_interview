from flask import Blueprint, jsonify, request
from services.generator import generator
import json

questions_bp = Blueprint('questions', __name__)

@questions_bp.route('/generate_questions', methods=['POST'])
def generate_questions_route():
    data = request.get_json()
    job_description = data.get('job_description', '')
    question_count = data.get('question_count', 15)
    question_format = data.get('question_format', 'qcm')
    
    if not job_description:
        return jsonify({"error": "Aucune offre d'emploi fournie"}), 400
    
    if question_count < 5 or question_count > 30:
        return jsonify({"error": "Le nombre de questions doit être entre 5 et 30"}), 400
    
    if question_format not in ['qcm', 'qa']:
        return jsonify({"error": "Format de question invalide. Choisissez 'qcm' ou 'qa'"}), 400
    
    print("⏳ Extraction des compétences clés...")
    tech_data = generator.extract_skills(job_description)
    print(f"✅ Compétences extraites: {json.dumps(tech_data, indent=2)}\n")
    
    print(f"⏳ Génération de {question_count} questions...")
    questions = generator.generate_questions(tech_data, question_count, question_format)
    print(f"✅ {len(questions)} questions générées\n")
    
    return jsonify({
        "questions": questions,
        "tech_data": tech_data,
        "stats": {
            "total_questions": len(questions),
            "languages_covered": len(set(q['skill'] for q in questions if q['category'] == 'langage')),
            "frameworks_covered": len(set(q['skill'] for q in questions if q['category'] == 'framework')),
            "concepts_covered": len(set(q['skill'] for q in questions if q['category'] == 'concept')),
            "soft_skills_covered": len(set(q['skill'] for q in questions if q['category'] == 'soft_skill'))
        }
    })