from flask import Flask
from flask_cors import CORS
from routes.questions import questions_bp
from routes.validation import validation_bp

app = Flask(__name__)

# Configuration CORS
CORS(app, resources={
    r"/generate_questions/*": {
        "origins": "http://localhost:5173",
        "methods": ["OPTIONS", "POST"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    },
    r"/validate_answer": {
        "origins": "http://localhost:5173",
        "methods": ["OPTIONS", "POST"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Enregistrement des blueprints
app.register_blueprint(questions_bp)
app.register_blueprint(validation_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)