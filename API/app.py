from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import random

app = Flask(__name__)
CORS(app)

'''
# User class

class User:
    def __init__(self, user_id, name, password, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = self.hash(password)
    
    # TODO: Write the hashing function
    def hash(self, password):
        return password

# Existing home endpoint
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Phishing Detection API!"})
'''

database = {}

@app.route('/email/score', methods=['GET'])
@cross_origin()
def get_score():
    new_score = random.randint(0, 100)
    return jsonify({'score': new_score})

# /classify endpoint
@app.route('/classify', methods=['POST'])
def classify_email():
    data = request.get_json()
    email_subject = data.get('email_subject')
    email_body = data.get('email_body')

    # Placeholder for AI classification logic
    classification = "phishing" if "reset" in email_body.lower() else "legitimate"
    confidence_score = 0.95 if classification == "phishing" else 0.85
    issues = ["Suspicious link detected"] if classification == "phishing" else []

    # Stores our results in the mock database
    email_id = len(database) + 1
    database[email_id] = {
        "classification": classification,
        "confidence_score": confidence_score,
        "issues": issues
    }

    return jsonify({
        "email_id": email_id,
        "classification": classification,
        "confidence_score": confidence_score,
        "issues": issues
    }), 201

# /results/<email_id> endpoint
@app.route('/results/<int:email_id>', methods=['GET'])
def get_results(email_id):
    result = database.get(email_id)
    if not result:
        return jsonify({"error": "Email ID not found"}), 404

    return jsonify(result)

# /status endpoint
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "running",
        "uptime": "24 hours",
        "total_emails_processed": len(database)
    })

# /delete/<email_id> endpoint
@app.route('/delete/<int:email_id>', methods=['DELETE'])
def delete_result(email_id):
    if email_id not in database:
        return jsonify({"error": "Email ID not found"}), 404

    del database[email_id]
    return jsonify({"message": f"Email with ID {email_id} has been deleted."})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
