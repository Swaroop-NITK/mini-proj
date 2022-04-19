
from flask import Flask, redirect, render_template,flash,request
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import VARCHAR
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user

# mydatabase connecction
local_server=True
app=Flask(__name__) 
app.secret_key="secretkey"

# this is for getting the unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return customer.query.get(int(user_id))

# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/databasename'3306
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost:3307/battery_swap'
db=SQLAlchemy(app)

#creating db models
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
 
class customer(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True)
    name=db.Column(db.String(40))
    dob=db.Column(db.String(1000))
    phone_number=db.Column(db.String(10),unique=True)

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/usersignup")
def usersignup():
    return render_template("usersignup.html")


@app.route("/alllogin")
def alllogin():
    return render_template("alllogin.html")



@app.route("/userlogin")
def userlogin():
    return render_template("userlogin.html")

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        email=request.form.get('email')
        name=request.form.get('name')
        dob=request.form.get('dob')
        phone_number=request.form.get('phone-number')
        # print(email,name,dob,phone_number)
        encpassword=generate_password_hash(dob)
        user=customer.query.filter_by(email=email).first()
        phone=customer.query.filter_by(phone_number=phone_number).first()
        if user or phone:
            flash("Email or phone number is already taken","warning")
            return render_template("usersignup.html")
        new_user=db.engine.execute(f"INSERT INTO `customer`(`email`,`name`,`dob`,`phone_number`) VALUES ('{email}','{name}','{encpassword}','{phone_number}')")
    
        flash("Signup Success, PLEASE LOGIN","success")
        return render_template("userlogin.html") 

    return render_template("usersignup.html")


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        email=request.form.get('email')
        dob=request.form.get('dob')
        user=customer.query.filter_by(email=email).first()
        if user and check_password_hash(user.dob,dob):
            login_user(user)
            flash("Login Success","info")
            return render_template("index.html")
        else:
            flash("Invalid Credentials","danger")
            return render_template("userlogin.html")


    return render_template("userlogin.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))


@app.route("/dealerlogin")
def dealerlogin():
    return render_template("dealerlogin.html")


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html") 

@app.route("/contactus")
def contactus():
    return render_template("contactus.html")   



# testing whether db is connected or not
@app.route("/test")
def test():
    try:
        a=customer.query.all()
        print(a)
        return f'MY DATABASE IS CONNECTED {a} '
    except Exception as e:
            print(e)
            return f'MY DATABASE IS NOT CONNECTED {e}'






app.run(debug=True) 
