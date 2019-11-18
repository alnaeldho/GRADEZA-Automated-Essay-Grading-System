
import pymysql.cursors
connection = pymysql.connect(host='localhost', user='root', password='', db='essay', charset='',  cursorclass=pymysql.cursors.DictCursor)
from flask import Flask, redirect, url_for,session,render_template
import flask
from main import session as session
from flask import flash

def excuteCommit(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        cursor.close()
    connection.commit()

def excuteselect(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

        k = cursor.fetchall()
        cursor.close()
        return k

def login(request):
    global session
    email =  request.form["email"]
    password = request.form["password"]
    print(email)
    print(password)
    if email == "admin" and password == "admin":
        print("admin logging")
        #return  flask.redirect("/admin-home")
        # return render_template("admin_home.html")
        return "admin"
    query = f"select  usertype from login where email = '{email}' and password = '{password}'"
    rows = excuteselect(query)
    print((rows))
    if len(rows) == 0:
        return "Invalid email Id or Password, Please Try again!"
    else:
        if rows[0]["usertype"] == "user":
            print("Setting User session")
            session['user']=email
            # return  flask.redirect("/user_home")
            #return render_template("user_home.html")
            return "user"
        

        

def forgot1(request):
    global session
    email =  request.form["email"]
    session['email']=email
    #print(session['email'])
    query = f"select  * from login where email = '{email}'"
    rows = excuteselect(query)
    #print((rows))
    if len(rows) == 0:
        return False #flask.redirect("guest/forgot1.html?msg=Invalid Email Id.")
    else:
        email=rows[0]["email"]
        session['email']=email
        return True #flask.redirect("guest/forgot2.html")

def forgot2(request):
    global session
    email =  session['email']
    squestion =  request.form["squestion"]
    answer =  request.form["answer"]
    print(email)
    query = f"select * from login where email = '{email}' and s_question= '{squestion}' and answer= '{answer}'"
    print(query)
    rows = excuteselect(query)
    print((len(rows)))
    if len(rows) == 0:
        #return False
        print("Invalid")
        return("Invalid sequrity question or answer!")
        
        
    else:
        pwd=rows[0]["password"]
        print(pwd)
        
        return("Your password is " + pwd)
        print("valid")
        
        

def registerUser(request):
    name = request.form["Name"]
    email = request.form["Email"]
    phone = request.form["MobileNo"]
    gender = request.form["Gender"]
    address =  request.form["Address"]
    password=  request.form["Password"]
    dateofbirth=request.form["DateofBirth"]
    qualification=request.form["Qualification"]
    institution=request.form["Institution"]
    squestion =  request.form["squestion"]
    answer =  request.form["answer"]
    #if pass1 != pass2:
        #return "Password Doesn't Match, Please try again!"
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO user_registration (name,gender,dateofbirth,qualification,Institution,address,mobile,emailid) VALUES (%s, %s , %s, %s, %s, %s,%s,%s)"
        cursor.execute(sql, (name,gender,dateofbirth,qualification,institution,address,phone,email))
    connection.commit()
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO login (email,password,usertype,status,s_question,answer) VALUES (%s, %s , %s, %s, %s, %s)"
        cursor.execute(sql, (email, password, 'user', 'pending',squestion,answer))
    connection.commit()
    return "Account Sussessfully Created, Please wait for the admin approval to login!"


