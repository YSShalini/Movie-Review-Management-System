from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configurations
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YSshalini@09',
    'database': 'moviereview'
}

conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template('h1.html')

@app.route('/loading', methods=['GET', 'POST'])
def loading():
    if request.method == 'POST':
        # Here you can handle your login logic if needed
        return render_template('loading.html')
    return redirect(url_for('h1'))

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor.execute('SELECT * FROM users WHERE name = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        
        if account:
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username/password!', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form and 'age' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        
        if account:
            flash('Email already registered!', 'danger')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'danger')
        elif not username or not email or not password or not age:
            flash('Please fill out the form!', 'danger')
        elif int(age) < 18:
            flash('Age must be greater than 18!', 'danger')
        else:
            cursor.execute('INSERT INTO users (name, email, password, age) VALUES (%s, %s, %s, %s)', (username, email, password, age,))
            conn.commit()
            flash('You have successfully registered!', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
