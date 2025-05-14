from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/images' # folder para jy picture nga i upload

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  
    database="studentinfo-sys-final"
)
cursor = db.cursor(dictionary=True)


@app.route('/') # login page
def index():
    return render_template('log.html', message='')

@app.route('/log', methods=['GET', 'POST']) 
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            session['user'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            message = 'Invalid username or password'

    return render_template('log.html', message=message)

@app.route('/sign', methods=['GET', 'POST']) # sign up page
def signup():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            message = 'Username already exists.'
            return render_template('sign.html', message=message)

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return redirect(url_for('login'))

    return render_template('sign.html', message=message)

@app.route('/homepage') #homepage
def dashboard():
    if 'user' in session:
        cursor.execute("SELECT * FROM student_info")
        students = cursor.fetchall()
        return render_template('homepage.html', user=session['user'], students=students)
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST']) #add student
def add_student():

    if request.method == 'POST':
        lname = request.form['lname']
        fname = request.form['fname']
        mname = request.form['mname']
        course = request.form['course']
        year = request.form['year']
        addedby = session.get('user')

        # Handle photo upload
        photo = request.files.get('photo')
        photo_filename = None
        if photo and photo.filename != '':
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_filename = filename

        cursor.execute(
            "INSERT INTO student_info (lname, fname, mname, course, year, addedby, photo) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (lname, fname, mname, course, year, addedby, photo_filename)
        )
        db.commit()
        return redirect(url_for('dashboard'))

    return render_template('add.html')

@app.route('/delete_student/<int:id>', methods=['GET']) #delete student
def delete_student(id):
    if 'user' not in session:
        return redirect(url_for('index'))

    cursor.execute("SELECT photo FROM student_info WHERE id = %s", (id,))
    student = cursor.fetchone()
    if student and student['photo']:
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], student['photo'])
        if os.path.exists(photo_path):
            os.remove(photo_path)

    cursor.execute("DELETE FROM student_info WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/update_student', methods=['POST']) #update student
def update_student():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    id = request.form.get('id')
    lname = request.form.get('lname')
    fname = request.form.get('fname')
    mname = request.form.get('mname')
    course = request.form.get('course')
    year = request.form.get('year')
    addedby = session.get('user')

    # Handle optional new photo
    photo = request.files.get('photo')
    if photo and photo.filename != '':
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cursor.execute("""
            UPDATE student_info 
            SET lname=%s, fname=%s, mname=%s, course=%s, year=%s, addedby=%s, photo=%s 
            WHERE id=%s
        """, (lname, fname, mname, course, year, addedby, filename, id))
    else:
        cursor.execute("""
            UPDATE student_info 
            SET lname=%s, fname=%s, mname=%s, course=%s, year=%s, addedby=%s
            WHERE id=%s
        """, (lname, fname, mname, course, year, addedby, id))

    db.commit()

    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
