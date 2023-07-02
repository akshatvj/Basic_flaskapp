from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AkshatVj'

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/add_student')
def add_student():
   return render_template('add_students.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         db = sql.connect("student_database.db")
         roll = request.form['roll']
         name = request.form['name']
         college = request.form['college']
         branch = request.form['branch']
         year = request.form['year']
         
         cur = db.cursor()
         cur.execute("INSERT INTO students (roll, name, college, branch, year) VALUES (?,?,?,?,?)",(roll, name, college, branch, year) )
         db.commit()
         msg = "Record successfully added!"
      except:
         db.rollback()
         msg = "error in insert operation"
      
      finally:
         db.row_factory = sql.Row
         cur = db.cursor()
         cur.execute("select * from students")
         students = cur.fetchall();
         return render_template("list.html", students = students, msg = msg)
         db.close()

@app.route('/list')
def list():
   db = sql.connect("student_database.db")
   db.row_factory = sql.Row
   
   cur = db.cursor()
   cur.execute("select * from students")
   
   students = cur.fetchall();
   return render_template("list.html", students = students)

if __name__ == '__main__':
    app.run(debug=True, port=8080) 
  