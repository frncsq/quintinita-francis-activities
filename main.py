from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key' 


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  
    database="student_info_sys"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    return render_template('login.html', message='')

@app.route('/login', methods=['GET', 'POST'])
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

    return render_template('login.html', message=message)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            message = 'Username already exists. Please try another.'
            return render_template('signup.html', message=message)

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return redirect(url_for('login'))

    return render_template('signup.html', message=message)

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        cursor.execute("SELECT * FROM student_info")
        students = cursor.fetchall()
        return render_template('home.html', user=session['user'], students=students)
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        lname = request.form['lname']
        fname = request.form['fname']
        mname = request.form['mname']
        course = request.form['course']
        year = request.form['year']
        added_by = session.get('user')

        cursor.execute(
            "INSERT INTO student_info (lname, fname, mname, course, year, added_by) VALUES (%s, %s, %s, %s, %s, %s)",
            (lname, fname, mname, course, year, added_by)
        )
        db.commit()
        return redirect(url_for('dashboard'))

    return render_template('add_student.html')

@app.route('/delete_student/<int:id>', methods=['GET'])
def delete_student(id):
    cursor.execute("DELETE FROM student_info WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/get_student_data/<int:id>', methods=['GET'])
def get_student_data(id):
    cursor.execute("SELECT * FROM student_info WHERE id = %s", (id,))
    student = cursor.fetchone()

    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route('/update_student', methods=['POST'])
def update_student():
    data = request.get_json()
    id = data.get('id')
    lname = data.get('lname')
    fname = data.get('fname')
    mname = data.get('mname')
    course = data.get('course')
    year = data.get('year')
    added_by = data.get('added_by')

    cursor.execute("""
        UPDATE student_info
        SET lname = %s, fname = %s, mname = %s, course = %s, year = %s, added_by = %s
        WHERE id = %s
    """, (lname, fname, mname, course, year, added_by, id))
    db.commit()

    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
