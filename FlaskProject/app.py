import requests
from flask import Flask, session, render_template, request, redirect, url_for
import pyrebase

# TODO 1: add your firebase project config
# Follow the youtube tutorial linked in the `README.md`
config = {
    'apiKey': "",
    'authDomain': "",
    'projectId': "",
    'storageBucket': "",
    'messagingSenderId': "",
    'appId': "",
    'measurementId': "",
    'databaseURL': ''
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = Flask(__name__)
# TODO 2: generate a strong secret key
# You can open a new terminal and copy+paste this code 
# python -c 'import secrets; print(secrets.token_hex())'
# Place the output as the value for app.secret_key
# We need the secret key to make our server-side session secure
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    if 'user' in session:
        # Massive shoutout to MohammadReza Keikavousi for the fakestoreapi
        fake_store = requests.get("https://fakestoreapi.com/products?limit=20")
        
        return render_template('index.html', fake_store=fake_store.json())
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return "Missing email or password", 400 
        
        try:
            # TODO 3: sign in user using pyrebase and name the variable as 'user'

            # set user session  
            session['user'] = user['email']
            
            return redirect(url_for('home'))
        
        except:
            return 'Failed to login', 500
        
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return "Missing email or password", 400 
        
        try:
            # TODO 4: create user using pyrebase and name the variable as 'user'

            # add user to session
            session['user'] = user['email']

            return redirect(url_for('home'))

        except:
            return 'Failed to signup', 500
        
    return render_template('signup.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login')) 

if __name__ == '__main__':
    app.run(debug=True, port=5000)