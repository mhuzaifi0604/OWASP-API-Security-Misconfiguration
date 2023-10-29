from flask import Flask, render_template, request, jsonify
import jwt
import datetime
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'Security Misconfig 420'

users = []
allowed_algorithms = ["none", "HS256", "HS384", "HS512"]

@app.route('/')
def index():
    return render_template('index.html')

@app.get('/server-data')
def server_data():
    return users

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')

    users.append({'username': username, 'password': password})

    # Encode the username and password as Base64
    encoded_username = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    encoded_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')

    # Create a payload dictionary with the Base64-encoded username and password
    payload = {
        "username": encoded_username,
        "password": encoded_password,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }

    # Encode the payload as a JWT
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm=allowed_algorithms[1])

    # Encode the whole token in Base64 before sending it to the frontend
    encoded_token = base64.b64encode(token.encode('utf-8')).decode('utf-8')

    print(f"Received data - Username: {username}, Password: {password}")

    return jsonify({'token': encoded_token})

@app.route('/validate', methods=['POST'])
def validate():
    token = request.form.get('token')
    loginusername = request.form.get('username')
    loginpassword = request.form.get('password')

    print("Username : ", loginusername, "\nPassword: ", loginpassword, "\nReceived Encoded Token :", token, "\n")

    try:
        # Decode the Base64-encoded token
        decoded_token = base64.b64decode(token).decode('utf-8')

        # Decode the JWT
        decoded = jwt.decode(decoded_token, options={"verify_signature": False}, algorithms=allowed_algorithms)

        token_username = base64.b64decode(decoded['username']).decode('utf-8')
        token_password = base64.b64decode(decoded['password']).decode('utf-8')

        print("Printing All Values ", token, decoded_token, token_username, token_password, loginusername, loginpassword)

        # if token_username == loginusername and token_password == loginpassword:
        for user in users:
            if user['username'] == loginusername and user['password'] == loginpassword:
                return jsonify({'message': 'Valid token && User Validated Successfully!'})

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'})
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'})

    return jsonify({'message': 'Invalid token or user not found'})

if __name__ == '__main__':
    app.run(debug=True)
