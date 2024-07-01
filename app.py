import json
from flask import Flask, jsonify, request
import re,joblib
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
def character(inputs):
    characters = []
    for i in inputs:
        characters.append(i)
    return characters
model = joblib.load('model_joblib1')
app = Flask(__name__)


@app.route('/PasswordStrengthChecker', methods=['POST'])
def check_password_strength():
    if request.is_json:
        data = request.get_json()
        password = data.get('password')
        
        if not password:
            return jsonify({ 'error': 'Password not provided'}), 400
        
        # Check password strength (example criteria: length >= 8 characters)
        is_strong = int(passwordchecker(password))
        
        return jsonify({ 'is_strong': is_strong })
    else:
        return jsonify({ 'error': 'Request must be JSON'}), 400

def passwordchecker(password):

    uppercase_regex = re.compile(r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]')
    lowercase_regex = re.compile(r'[abcdefghijklmnopqrstuvwxyz]')
    number_regex = re.compile(r'\d')
    special_regex = re.compile(r'\W')
    uppercase_check = uppercase_regex.search(password)
    lowercase_check = lowercase_regex.search(password)
    number_check = number_regex.search(password)
    special_check = special_regex.search(password)
    strong = ''
    if (uppercase_check == None) == True | (lowercase_check == None) == True | (number_check == None) == True | (
            special_check == None) == True:
        strong = 0
    elif len(password) < 8:
        strong = 0
    else:
        val = (model.predict([password]))
        strong = val[0]
    return strong # Example criteria: at least 8 characters

# Example of running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
