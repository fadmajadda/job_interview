import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# 1) Load all variables from backend/.env into environment
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

app = Flask(__name__)

# 2) Read the comma-separated list from the environment
cors_env = os.getenv("FLASK_CORS_ALLOWED_ORIGINS", "")
allowed_origins = [o.strip() for o in cors_env.split(",") if o.strip()]

# 3) Pass that list into CORS
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
        }
    },
)

from routes.questions import questions_bp
from routes.validation import validation_bp

app.register_blueprint(questions_bp, url_prefix="/api")
app.register_blueprint(validation_bp, url_prefix="/api")

if __name__ == "__main__":
    port = int(os.getenv("FLASK_INTERNAL_PORT", 5000))
    app.run(debug=True, port=port)
