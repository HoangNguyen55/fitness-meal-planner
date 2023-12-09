import requests
from flask import Flask, request, jsonify, send_from_directory
from ai import AI


ai = AI()

app = Flask(__name__)
AI_ENDPOINT = "https://0268-174-173-174-219.ngrok-free.app/ask_ai"
@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/ask_ai", methods=["GET"])
def get_ai():
    # This is just for testing purposes
    return "This is the GET response from /ask_ai. Please use POST to send data."
@app.route("/ask_ai", methods=["POST"])
def ask_ai_endpoint():
    print("Received request for AI processing")
    try:
        data = request.get_json(force=True)
        print("Data received:", data)

        # Convert height and weight to float
        try:
            data["height"] = float(data["height"])
            data["weight"] = float(data["weight"])
        except ValueError:
            return jsonify({"error": "Height and Weight must be numbers."}), 400

        # Validate height as a positive number
        if data["height"] <= 0:
            return jsonify({"error": "Height must be a positive number."}), 400

        # Validate sex as 'male' or 'female'
        if data["sex"] not in ["male", "female"]:
            return jsonify({"error": "Invalid sex. Choose 'male' or 'female'."}), 400

        # Validate activity level as 'low', 'medium', or 'high'
        if data["activity"] not in ["low", "medium", "high"]:
            return jsonify({"error": "Invalid activity level. Choose 'low', 'medium', or 'high'."}), 400

        # Validate goals as 'lose', 'gain', or 'maintain'
        if data["goals"] not in ["lose", "gain", "maintain"]:
            return jsonify({"error": "Invalid goals. Choose 'lose', 'gain', or 'maintain'."}), 400

        # Forward the request to the external AI service
        response = requests.post(AI_ENDPOINT, json=data)
        # Log the response status and content for debugging
        print("External service response:", response.status_code, response.content)
        # Check if the request to the external service was successful
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "External AI service error", "status_code": response.status_code}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6731, debug=True)
