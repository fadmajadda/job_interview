from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json
from typing import Dict, List
import random
import re

app = Flask(__name__)
CORS(app)

# Configurez votre API Key
genai.configure(api_key="AIzaSyCAmDVW5ETCqhc-aoxsUHELM9AHmyTZx5E")  

class InterviewGenerator:
    def __init__(self):
        self.extraction_model = genai.GenerativeModel('gemini-1.5-flash')
        self.generation_model = genai.GenerativeModel('gemini-1.5-pro')
        self.language_map = {
            'fr': 'french',
            'en': 'english',
            'es': 'spanish',
            'de': 'german',
            'it': 'italian'
        }

    def detect_language(self, text: str) -> str:
        """Détecte la langue principale du texte"""
        prompt = f"""
        Identifie la langue principale de ce texte. 
        Réponds UNIQUEMENT avec le code langue (fr, en, es, de, it).
        
        Texte: {text[:1000]}
        """
        try:
            response = self.extraction_model.generate_content(prompt)
            return response.text.strip().lower()
        except Exception as e:
            print(f"Erreur de détection de langue: {e}")
            return 'fr'  # Retourne français par défaut en cas d'erreur

    def extract_skills(self, job_description: str) -> Dict:
        """Extrait les compétences techniques et détecte la langue"""
        try:
            language = self.detect_language(job_description)
            
            prompt = f"""
            Analyse cette offre d'emploi et extrais les informations suivantes au format JSON.
            La langue détectée est {language}.
            
            {job_description}

            Format de sortie:
            {{
                "language": "{language}",
                "languages": ["liste", "des", "langages"],
                "frameworks": ["liste", "des", "frameworks"],
                "tools": ["liste", "des", "outils"],
                "concepts": ["liste", "des", "concepts techniques"],
                "level": "junior/mid/senior",
                "soft_skills": ["liste", "des", "compétences", "douces"]
            }}
            """
            
            response = self.extraction_model.generate_content(prompt)
            data = self._parse_json(response.text)
            data['language'] = language
            return data
        except Exception as e:
            print(f"Erreur d'extraction des compétences: {e}")
            return {
                "language": "fr",
                "languages": [],
                "frameworks": [],
                "tools": [],
                "concepts": [],
                "level": "mid",
                "soft_skills": []
            }

    def generate_questions(self, tech_data: Dict, question_count: int = 15, question_format: str = 'qcm') -> List[Dict]:
        """Génère plusieurs questions techniques avec réponses"""
        try:
            language = tech_data.get('language', 'fr')
            lang_name = self.language_map.get(language, 'french')
            
            format_instruction = ""
            if question_format == 'qcm':
                format_instruction = """
                5. Une seule réponse correcte par question (placée aléatoirement)
                6. Les mauvaises réponses doivent être plausibles
                7. Les explications doivent être claires et pédagogiques

                **Format de sortie STRICT**:
                [
                    {
                        "category": "langage/concept/outil/soft_skill",
                        "skill": "nom de la compétence évaluée",
                        "question": "texte de la question",
                        "options": [
                            {"text": "réponse 1", "correct": false},
                            {"text": "réponse 2", "correct": true},
                            {"text": "réponse 3", "correct": false},
                            {"text": "réponse 4", "correct": false},
                            {"text": "réponse 5", "correct": false}
                        ],
                        "explication": "Explication détaillée de la réponse correcte",
                        "difficulty": "facile/moyen/difficile"
                    },
                    // Plus de questions...
                ]
                """
            else:
                format_instruction = """
                5. Fournir une réponse détaillée et une explication claire
                6. Les questions doivent être ouvertes et stimulantes

                **Format de sortie STRICT**:
                [
                    {
                        "category": "langage/concept/outil/soft_skill",
                        "skill": "nom de la compétence évaluée",
                        "question": "texte de la question",
                        "answer": "Réponse détaillée à la question",
                        "explication": "Explication approfondie de la réponse",
                        "difficulty": "facile/moyen/difficile"
                    },
                    // Plus de questions...
                ]
                """
            
            prompt = f"""
            Tu es un expert en recrutement technique. Génère un questionnaire complet de {question_count} questions en {lang_name} pour évaluer 
            un candidat de niveau {tech_data.get('level', 'mid')} sur TOUTES les compétences suivantes:
            
            Compétences techniques:
            - Langages: {tech_data.get('languages', [])}
            - Frameworks: {tech_data.get('frameworks', [])}
            - Outils: {tech_data.get('tools', [])}
            - Concepts: {tech_data.get('concepts', [])}
            
            Compétences non-techniques:
            - Soft skills: {tech_data.get('soft_skills', [])}

            **Instructions**:
            1. Génère exactement {question_count} questions couvrant TOUS les aspects clés
            2. Pour chaque élément technique important, génère au moins 2 questions
            3. Inclus 2-3 questions sur les soft skills (si {question_count} >= 10)
            4. Variété des types de questions (théorique, pratique, cas concret)
            {format_instruction}
            """
            
            response = self.generation_model.generate_content(prompt)
            return self._parse_questions(response.text, question_format)
        except Exception as e:
            print(f"Erreur de génération des questions: {e}")
            return [self._create_default_question(question_format)]

    def _parse_json(self, text: str) -> Dict:
        """Extrait le JSON de la réponse du modèle avec une méthode plus robuste"""
        try:
            # Nettoyage du texte pour enlever les marqueurs de code
            text = re.sub(r'```json|```', '', text).strip()
            return json.loads(text)
        except json.JSONDecodeError as e:
            print(f"Erreur de décodage JSON: {e}")
            # Tentative de récupération avec extraction entre {}
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

    def _parse_questions(self, text: str, question_format: str) -> List[Dict]:
        """Extrait la liste de questions de la réponse du modèle selon le format"""
        try:
            # Nettoyage du texte pour enlever les marqueurs de code
            text = re.sub(r'```json|```', '', text).strip()
            
            # Tentative de parsing direct
            try:
                questions = json.loads(text)
                return self._validate_questions(questions, question_format)
            except json.JSONDecodeError:
                pass
            
            # Si échec, tentative d'extraction entre []
            start = text.find('[')
            end = text.rfind(']') + 1
            if start != -1 and end != -1:
                questions = json.loads(text[start:end])
                return self._validate_questions(questions, question_format)
                
            # Si tout échoue, retourne une question par défaut
            print(f"Échec du parsing des questions. Contenu: {text[:500]}...")
            return [self._create_default_question(question_format)]
            
        except Exception as e:
            print(f"Erreur critique lors du parsing des questions: {e}")
            return [self._create_default_question(question_format)]

    def _validate_questions(self, questions: List, question_format: str) -> List[Dict]:
        """Valide la structure des questions et corrige si nécessaire"""
        valid_questions = []
        for q in questions:
            if not isinstance(q, dict):
                continue
                
            # Vérification des champs obligatoires
            if 'question' not in q:
                continue
                
            # Normalisation selon le format
            if question_format == 'qcm':
                if 'options' not in q:
                    continue
                    
                # Vérification qu'il y a exactement une réponse correcte
                correct_options = [opt for opt in q['options'] if isinstance(opt, dict) and opt.get('correct', False)]
                if len(correct_options) != 1:
                    # Tentative de correction en marquant la première option comme correcte
                    if q['options']:
                        q['options'][0]['correct'] = True
                        for opt in q['options'][1:]:
                            opt['correct'] = False
                    else:
                        continue
            else:
                if 'answer' not in q:
                    continue
                    
            # Ajout des champs manquants avec des valeurs par défaut
            q.setdefault('category', 'concept')
            q.setdefault('skill', 'Général')
            q.setdefault('explication', 'Explication non fournie')
            q.setdefault('difficulty', 'moyen')
            
            valid_questions.append(q)
            
        return valid_questions or [self._create_default_question(question_format)]

    def _create_default_question(self, question_format: str = 'qcm') -> Dict:
        """Crée une question par défaut en cas d'erreur"""
        if question_format == 'qcm':
            return {
                "category": "erreur",
                "skill": "erreur",
                "question": "Question par défaut (une erreur est survenue)",
                "options": [
                    {"text": "Réponse 1", "correct": True},
                    {"text": "Réponse 2", "correct": False},
                    {"text": "Réponse 3", "correct": False},
                    {"text": "Réponse 4", "correct": False},
                    {"text": "Réponse 5", "correct": False}
                ],
                "explication": "Une erreur est survenue lors de la génération des questions.",
                "difficulty": "moyen"
            }
        else:
            return {
                "category": "erreur",
                "skill": "erreur",
                "question": "Question par défaut (une erreur est survenue)",
                "answer": "Réponse par défaut",
                "explication": "Une erreur est survenue lors de la génération des questions.",
                "difficulty": "moyen"
            }

generator = InterviewGenerator()

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    data = request.get_json()
    job_description = data.get('job_description', '')
    question_count = data.get('question_count', 15)  # Valeur par défaut 15
    question_format = data.get('question_format', 'qcm')  # Nouveau paramètre
    
    if not job_description:
        return jsonify({"error": "Aucune offre d'emploi fournie"}), 400
    
    if question_count < 5 or question_count > 30:
        return jsonify({"error": "Le nombre de questions doit être entre 5 et 30"}), 400
    
    if question_format not in ['qcm', 'qa']:
        return jsonify({"error": "Format de question invalide. Choisissez 'qcm' ou 'qa'"}), 400
    
    print("⏳ Extraction des compétences clés...")
    tech_data = generator.extract_skills(job_description)
    print(f"✅ Compétences extraites: {json.dumps(tech_data, indent=2)}\n")
    
    print(f"⏳ Génération de {question_count} questions en {tech_data.get('language', 'fr')}...")
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
# Add this new endpoint right before the if __name__ == "__main__": block
@app.route('/validate_answer', methods=['POST'])
def validate_answer():
    data = request.get_json()
    question = data.get('question', {})
    user_answer = data.get('user_answer', '')
    
    if not question or not user_answer:
        return jsonify({"error": "Missing question or answer"}), 400
    
    try:
        # Get the correct answer from the question
        correct_answer = question.get('answer', '')
        
        prompt = f"""
        Evaluate if this answer is correct for the given question.
        Question: {question.get('question', '')}
        Correct Answer: {correct_answer}
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
        
        # Ensure all required fields are present
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
if __name__ == "__main__":
    app.run(debug=True, port=5000)