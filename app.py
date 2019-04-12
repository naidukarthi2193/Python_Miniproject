from flask import Flask, render_template, request
import sqlite3 as sql
import hashlib

app = Flask(__name__)


@app.route('/')
def home():
   return render_template('login_page.html')


@app.route('/newregister', methods=['POST', 'GET'])
def newregister():
   return render_template("newregister.html")


@app.route('/newregisterdone', methods=['POST', 'GET'])
def newregisterdone():
   msg="default"
   if request.method == 'POST':
      msg="posted"
      try:
         msg="tried"
         customerid = request.form['customerid']
         password = request.form['pass']

         # password = hashlib.sha256(password.encode()).hexdigest()
         print(password)
         name = request.form['name']
         credit = request.form['creditscore']
         location = request.form['location']
         age = request.form['age']
         gender = request.form['gender']
         tenure = request.form['tenure']
         balance = request.form['balance']

         products = request.form['products']
         card = request.form['credit']
         member = request.form['member']
         salary=request.form['salary']
         print("REacheddd")
         con=sql.connect("bank.db")
         cur=con.cursor()
         msg="reached"
         cur.execute("INSERT INTO login(username,password)VALUES(?, ?)",(customerid,password))
         msg="reached1"
         cur.execute("INSERT INTO employee(customerid,name,creditscore,location,gender,age,tenure,balance,products,card,member,salary)VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",(customerid,name,credit,location,gender,age,tenure,balance,products,card,member,salary))
         msg="reached2"
         con.commit()
         msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      finally:
         return render_template("result.html", msg=msg)
         con.close()


@app.route('/postlogin', methods=['POST', 'GET'])
def postlogin():
   if request.method == 'POST':
      try:
         customerid = request.form['customerid']
         password=request.form['password']
         # password=hashlib.sha256(password.encode()).hexdigest()
         print(customerid)
         print(password)
         con=sql.connect("bank.db")
         cur = con.cursor()
         cur.execute("SELECT * FROM login")
         rows = cur.fetchall()
         for row in rows:
            print(row[0])
            if customerid == row[0]:
               if password==row[1]:
                  con = sql.connect("bank.db")
                  con.row_factory = sql.Row
                  cur = con.cursor()
                  cur.execute("select * from employee")
                  rows = cur.fetchall();
                  break
            else:
               msg="Login Not Found"
      except:
         con.rollback()
         msg = "Login Error"
      finally:
         return render_template("employeelist.html", rows=rows)
         con.close()

if __name__ == '__main__':
   app.run(debug = True)