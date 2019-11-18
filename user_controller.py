
import pymysql.cursors
connection = pymysql.connect(host='localhost', user='root', password='', db='essay', charset='',  cursorclass=pymysql.cursors.DictCursor)
from flask import Flask, redirect, url_for, session
import flask
from datetime import date

from main import session as session

def excuteCommit(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
    connection.commit()

def excuteselect(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def addSiteVisitDetails(request):
    name = request.form["name"]
    itemname = request.form["item_name"]
    visit_date = request.form["visit_date"]
    address= request.form["address"]
    comments= request.form["comments"]
    query = f"insert into site_visit_details(user_name,item_name,visit_date,site_address,comments,status) values ('{name}','{itemname}','{visit_date}','{address}','{comments}','Pending')"
    return excuteCommit(query)

def addFeedback(request):
    global session
    username=session['customer']
    itemname = request.form["item_name"]
    description= request.form["description"]
    today_date=date.today()
   
    print(username)
    query = f"insert into feedback(user_name,item_name,description,date) values ('{username}','{itemname}','{description}','{today_date}')"
    return excuteCommit(query)

def addCart(request):
    global session
    username=session['customer']
    id = request.args.get("id")
    today_date=date.today()
    print("inside add cart")
    print(username)
    query = f"insert into cart(user_id,item_id,date) values ('{username}','{id}',{today_date}')"
    print(query)
    return excuteCommit(query)

def addEssay(request):
    global session
    username=session['user']
    id =session["id"]
    today_date=date.today()
    file = request.files['filename']
    filename=file.filename
    print(id)
    query = f"insert into essay_upload(email,date,essay_id,filename,status) values ('{username}','{today_date}','{id}','{filename}','not validated')"
    print(query)
    return excuteCommit(query)


    
def makeEssay(request):
    #global session
    itemname = ""
    #username=session['customer']
    id = request.args.get("id")
    session["id"]=id
    return id

def getItemDetails(request):
    #get item details with session
    id = request.args.get("id")
    query = f"select * from item where id = '{id}'"
    return excuteselect(query)

def getCartDetails(request):
    #get item details with session
    id = request.args.get("id")
    query = f"select item.* from item,cart where item.id = cart.item_id and item.id ='{id}'"
    return excuteselect(query)

def getMarketingDetails(request):
    query = f"select marketing.* from marketing"
    return excuteselect(query)
    
def getUnitPrice(request):
    #get item details with session
    id = request.args.get("id")
    query = f"select * from purchace_details where item_name= '{id}'"
    return excuteselect(query)
    

def getUserDetails():
    
    query = "select * from  users"
    return excuteselect(query)

def getEssayDetails():
    
    query = "select * from essay_keyword"
    return excuteselect(query)

def getScoreDetails():
    query="select score from essay_upload "