from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ask_ai', methods=['POST'])
def ask_ai_endpoint():
    try:
        # Get data from the POST request as JSON
        data = request.json
        
        # Extract user data
        height = data['height']
        sex = data['sex']
        goals = data['goals']
        activity = data['activity']
        
        # Data Validation and Transformation
        
        # Validate height as a positive number
        if not isinstance(height, (int, float)) or height <= 0:
            return jsonify({"error": "Height must be a positive number."}), 400
        
        # Validate sex as 'male' or 'female'
        if sex not in ['male', 'female']:
            return jsonify({"error": "Invalid sex. Choose 'male' or 'female'."}), 400
        
        # Validate activity level as 'low', 'medium', or 'high'
        if activity not in ['low', 'medium', 'high']:
            return jsonify({"error": "Invalid activity level. Choose 'low', 'medium', or 'high'."}), 400
        
        # Validate goals as 'lose', 'gain', or 'maintain'
        if goals not in ['lose', 'gain', 'maintain']:
            return jsonify({"error": "Invalid goals. Choose 'lose', 'gain', or 'maintain'."}), 400
        
        # At this point, data is valid, proceed to call the AI function
        
        # Call the AI function with user data
        ai_response = ask_ai(height, sex, goals, activity)

        # Return the AI's response to the client
        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Return an error response if something goes wrong

# Mocked-up AI function
def ask_ai(height, sex, goals, activity):
    # Replace this with your AI logic
    response = f"Received data: Height={height}, Sex={sex}, Goals={goals}, Activity={activity}"
    return response

if __name__ == '__main__':
    app.run(debug=True)
