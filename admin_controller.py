
import pymysql.cursors
connection = pymysql.connect(host='localhost', user='root', password='', db='essay', charset='',  cursorclass=pymysql.cursors.DictCursor)
from flask import Flask, redirect, url_for
import flask
from main import session as session
import language_check
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from datetime import date
def excuteCommit(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
    connection.commit()

def excuteselect(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def getPendingUsers():
    query = "select user_registration.* from user_registration,login where user_registration.emailid = login.email and login.status = 'pending'"
    return excuteselect(query)


def getComplaints():
    query = "select feedback.* from feedback"
    return excuteselect(query)

def approveUser(request):
    id = request.args.get("id")
    query = f"update login set status = 'approved' where email = '{id}'"
    return excuteCommit(query)





def addEssayDetails(request):
    
    topic = request.form["topic"]
    keywords= request.form["keywords"]
    rules= request.form["rules"]
    query = f"insert into essay_keyword(topic,keywords,rules) values ('{topic}','{keywords}','{rules}')"
    return excuteCommit(query)




def addEssay(request):
    global session
    username=session['user']
    id = request.args.get("essayid")
    today_date=date.today()
    filename= request.form["filename"]
    print(username)
    query = f"insert into essay_upload(email,date,essay_id,filename,status) values ('{username}','{today_date}','{id}','{filename}','not validated')"
    print(query)
    return excuteCommit(query)

def similaritycalculate(X,Y):

    # tokenization 
    X_list = word_tokenize(X)  
    Y_list = word_tokenize(Y) 
  
    # sw contains the list of stopwords 
    sw = stopwords.words('english')  
    l1 =[];l2 =[] 
  
    # remove stop words from string 
    X_set = {w for w in X_list if not w in sw}  
    Y_set = {w for w in Y_list if not w in sw} 
  
    # form a set containing keywords of both strings  
    rvector = X_set.union(Y_set)  
    for w in rvector: 
        if w in X_set: l1.append(1) # create a vector 
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 
    c = 0
  
    # cosine formula  
    for i in range(len(rvector)): 
        c+= l1[i]*l2[i] 
    cosine = c / float((sum(l1)*sum(l2))**0.5) 
    #print("similarity: ", cosine) 
    return(cosine)



def calcScore(request):
    path= "./static/Upload_images"
    query = "select essay_upload.* , essay_keyword.keywords from essay_upload ,essay_keyword where essay_upload.essay_id= essay_keyword.id and essay_upload.status = 'not validated'"
    rows = excuteselect(query)
    print((rows))
    if len(rows) == 0:
        return "Invalid"
    else:
        for item in rows:
            # print("ffgfffffgfgghttht")
            print("row is" ,item)
            upload_id=item["id"]
            essay_file=item["filename"]
            file_read= path +"/"+essay_file
            essayContent = ""
            filehandle= ""
            #with open(file_read,'r'):
            filehandle = open(file_read, 'r')
            essayContent = filehandle.readlines()
            filehandle.close()
            content=""
            content=' '.join([str(elem) for elem in essayContent])
            e=type(content)
            # print("type",e)
            
            # print("content",content)
            keywords= ""
            keywords=item["keywords"]
            k=type(keywords)
            # print("type",k)
            # print("keywords",keywords)
            score= similaritycalculate(content,keywords)
            grade=""
            print(score)
           
            print(grade)
            if score>=0.08:
               grade='A+'
            elif 0.06<=score<0.08:
                grade='A'
            elif 0.04<=score<0.06:
                grade='B'
            else:
                grade='C'
            print(grade)
            query = f"update essay_upload set score='{grade}',status ='validated' where id='{upload_id}'"
            print(query)
            excuteCommit(query)


