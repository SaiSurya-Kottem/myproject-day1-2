from flask import *
import mysql.connector
import os
import csv

app=Flask(__name__)
myconn = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="college"
)




@app.route("/")
@app.route("/home")
def home():
	return render_template("index.html",name="sai")

@app.route("/register",methods=['GET','POST'])
def register():
	if request.method == "POST":
		rollno=request.form['rollno']
		name=request.form['name']
		email=request.form['email']
		phno=request.form['phno']
		college=request.form['college']
		branch=request.form['branch']
		section=request.form['section']
		gen=request.form['gender']
		lan=request.form.getlist('lan')
		lan=','.join(lan)
		mycur=myconn.cursor()
		mycur.execute("select * from students where rollno=(%s)"%(rollno))
		data=mycur.fetchall()
		
		if len(data)==0:
			mycur.execute("""insert into students(rollno,name,
				college,branch,section,email,phno,gender,languages)
				values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
				(rollno,name,college,branch,section,email,phno,gen,lan))

			myconn.commit()
		else:
			print("already inserted")
		return redirect(url_for('register'))

	else:
		return render_template("about.html")
	

@app.route("/view",methods=['GET','POST'])
def view():
	cur=myconn.cursor()
	cur.execute("select * from students")
	data=cur.fetchall()
	return render_template("view.html",data=data)

@app.route("/delete",methods=['GET','POST'])
def delete():
	if request.method == "POST":
		id=request.form['delete']
		cur=myconn.cursor()
		cur.execute("delete from students where sno=%s"%(id))
		myconn.commit()
		return redirect(url_for('view'))

@app.route("/edit",methods=['GET','POST'])
def edit():
	if request.method == "POST":
		id=request.form['edit']
		cur=myconn.cursor()
		cur.execute("select * from students where sno=%s"%(id))
		data=cur.fetchall()
		lan=data[0][-1].split(',')
		return render_template("edit.html",data=data,lan=lan)

@app.route("/update",methods=['GET','POST'])
def update():
	if request.method == "POST":
		id=request.form['id']
		rollno=request.form['rollno']
		name=request.form['name']
		email=request.form['email']
		phno=request.form['phno']
		college=request.form['college']
		branch=request.form['branch']
		section=request.form['section']
		gen=request.form['gender']
		lan=request.form.getlist('lan')
		lan=','.join(lan)
		mycur=myconn.cursor()
		mycur.execute("""update students set rollno=%s,
			name=%s,email=%s,phno=%s,college=%s,branch=%s,section=%s,
			gender=%s,languages=%s where sno=%s""",
			(rollno,name,email,phno,college,branch,section,gen,lan,id))
		myconn.commit()
		return redirect(url_for('view'))

if __name__ =="__main__":
	app.run(debug=True)

