from static.py.DiseasePredictor import DiseasePredictor

from flask import Flask, request, render_template, jsonify, redirect, url_for, session # Import jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

# flask app
app = Flask(__name__)

app.secret_key = 'abcdef'

#my configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Samk@sql55'
app.config['MYSQL_DB'] = 'chikitsalogin'
 
mysql = MySQL(app)

# creating routes========================================

#home route
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/About")
def about():
    return render_template("about.html")

@app.route("/Contacts")
def contacts():
    return render_template("contacts.html")

@app.route("/Recommendation")
def recommendation():
    return render_template("recommendation.html")

@app.route("/Consult")
def consult():
    return render_template("consult.html")

@app.route("/Yoga")
def yoga():
    return render_template("yoga.html")

@app.route("/Shop")
def shop():
    return render_template("shop.html")

@app.route("/Profile")
def profile():
    return render_template("profile.html")


# login & reg. routes========================================

@app.route('/Login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('profile.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/Logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
 
@app.route('/Register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)









#displaying data 

@app.route("/process_data", methods=["POST"])
def process_data():
    data = request.json.get("data")
    predictor = DiseasePredictor()
    predicted_disease = predictor.predict_disease(data)
    disease_description, precautions_list, remedies_list, diet_list, workout_list = predictor.get_disease_details(predicted_disease)
    
    return jsonify({
        "disease_name": predicted_disease,
        "diet_list": diet_list,
        "workout_list": workout_list,
        "remedies_list": remedies_list,
        "precautions_list": precautions_list,
        "disease_description": disease_description
    })


if __name__ == '__main__':

    app.run(debug=True)