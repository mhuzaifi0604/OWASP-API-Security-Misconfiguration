from flask import Flask, render_template, request, jsonify
import jwt
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5500"}})
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
    
    # Do something with the received data (e.g., validate and process it)
    # For this example, we'll just print the data to the console
    payload = {
        "username": username,
        "password": password,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    print(f"Received data - Username: {username}, Password: {password}")
    
    return jsonify({'token': token})

@app.route('/validate', methods=['POST'])
def validate():
    token = request.form.get('token')
    print("Token Recieved from frontend: ", token)
    try:
        decoded = jwt.decode(token, options={"verify_signature": False}, algorithms=allowed_algorithms)
        print(decoded)
        return jsonify({'message': 'Valid token'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'})

if __name__ == '__main__':
    app.run(debug=True)
