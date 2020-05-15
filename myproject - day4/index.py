
from flask import *
import mysql.connector
from werkzeug.utils import secure_filename
import os
import csv

app=Flask(__name__)
app.secret_key="dnt tell" 
UPLOAD_FOLDER='./static/data'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER


myconn = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="college"
)

@app.route("/")
@app.route("/login",methods=['GET','POST'])
def login():
	if request.method=="POST":
		uname=request.form['uname']
		pwd=request.form['pwd']
		cur=myconn.cursor()
		cur.execute("""select * from admin where 
			username=%s and password=%s""",(uname,pwd))
		data=cur.fetchall()
		if data:
			session['loggedin']=True
			flash("Login Successfully")
			return render_template("index.html")
		else:
			flash("Incorrect Username or Password")
	return render_template("login.html")


@app.route("/home")
def home():
	if not session.get('loggedin'):
		return render_template("login.html")

	return render_template("index.html")

@app.route("/register",methods=['GET','POST'])
def register():
	if not session.get('loggedin'):
		return render_template("login.html")

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
			flash("Registered Successfully")

		else:
			flash("Already Registered")
		return redirect(url_for('register'))

	else:
		return render_template("about.html")
	

@app.route("/view",methods=['GET','POST'])
def view():
	if not session.get('loggedin'):
		return render_template("login.html")
	cur=myconn.cursor()
	cur.execute("select * from students")
	data=cur.fetchall()
	return render_template("view.html",data=data)

@app.route("/delete",methods=['GET','POST'])
def delete():
	if not session.get('loggedin'):
		return render_template("login.html")
	if request.method == "POST":
		id=request.form['delete']
		cur=myconn.cursor()
		cur.execute("delete from students where sno=%s"%(id))
		myconn.commit()
		flash("Deleted Successfully")
		return redirect(url_for('view'))

@app.route("/edit",methods=['GET','POST'])
def edit():
	if not session.get('loggedin'):
		return render_template("login.html")
	if request.method == "POST":
		id=request.form['edit']
		cur=myconn.cursor()
		cur.execute("select * from students where sno=%s"%(id))
		data=cur.fetchall()
		lan=data[0][-1].split(',')
		return render_template("edit.html",data=data,lan=lan)

@app.route("/update",methods=['GET','POST'])
def update():
	if not session.get('loggedin'):
		return render_template("login.html")
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


@app.route("/bulk",methods=['GET','POST'])
def bulk():
	if not session.get('loggedin'):
		return render_template("login.html")
	if request.method=="POST":
		file=request.files['data']
		name=file.filename
		ext=name.split('.')
		mycur=myconn.cursor()
		if ext[-1]=='csv':
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
			with open("static/data/"+name) as f1:
				records=list(csv.reader(f1))
				if len(records[0])!=9:
					flash("invalid CSV file")
				else:

					for record in records[1:]:
						mycur.execute("""insert into students(rollno,name,
					college,branch,section,email,phno,gender,languages)
					values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
					(record[0],record[1],record[2],record[3],
						record[4],record[5],record[6],record[7],record[8]))

						myconn.commit()


		else:
			flash('Incorrect flie type')
	return render_template("bulk.html")



@app.route("/logout")
def logout():
	session['loggedin']=False
	return render_template("login.html")


if __name__ =="__main__":
	app.run(debug=True)