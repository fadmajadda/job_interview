from flask import Flask
from flask_cors import CORS
from routes.questions import questions_bp
from routes.validation import validation_bp

app = Flask(__name__)
allowed_origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://localhost:3000",
]

# Configuration CORS
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],  # Example: if you use auth headers
            "supports_credentials": True,
        }
    },
)

app.register_blueprint(questions_bp, url_prefix="/api")
app.register_blueprint(validation_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
