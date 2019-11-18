import os
from flask import Flask, render_template,  redirect, url_for, request,  flash, session
from werkzeug.utils import secure_filename
from datetime import date
session={}
import guest_controller
import admin_controller

import user_controller
UPLOAD_FOLDER = './static/Upload_images/'
ALLOWED_EXTENSIONS = set(['docx'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
   
app.secret_key="admin"

@app.route('/',methods = ['POST', 'GET']) #decorator drfines the   
def home():
    return render_template("index.html")

    #global session
    # msg = ""
    #if request.method == 'POST':
        #msg = guest_controller.login(request)
    #if "Response" in str(msg):
       # return msg
    #if "DOCTYPE" in str(msg):
        #return msg


@app.route('/pre-signup')
def pre_signup():  
    return render_template("Registration.html")

@app.route('/login',methods = ['POST', 'GET'])
def login(): 
    msg = ""
    if request.method == 'POST':
        msg = guest_controller.login(request)
        if msg=="admin":
            return render_template("admin_home.html")
        if msg=="user":
            return render_template("user_home.html")
        
    return render_template("index.html",message=msg)


@app.route('/forgot')
def forgot():  
    return render_template("guest/forgot1.html")

@app.route('/user-signup',methods = ['POST', 'GET'])
def user_signup():
    msg = ""
    if request.method == 'POST':
        print("inside post")
        msg = guest_controller.registerUser(request)
    return render_template("Registration.html",message=msg)

@app.route('/comparision',methods = ['POST', 'GET'])
def comparision():
    msg = ""
    print("dfdgd")
    # if request.method == 'POST':
    print("inside post")
    msg = admin_controller.calcScore(request)
    return render_template("comparision.html",message=msg)


@app.route('/forgot_pwd1',methods = ['POST', 'GET'])
def forgot_pwd1():
    msg = ""
    #print ("b4 post")
    if request.method == 'POST':
        print("in post")
        msg = guest_controller.forgot1(request)
        #print("MMMSSSSSSSSSSSSSSSSSGGGGGG = ", msg)
        if msg:    
            return render_template("guest/forgot2.html",message='')
        else:
            return render_template("guest/forgot1.html",message="Email Id Not registered!")
    return render_template("guest/forgot2.html",message='')
@app.route('/add_vendor',methods = ['POST', 'GET'])
def add_vendor():
    msg = ""
    if request.method == 'POST':
        msg = admin_controller.addVendor(request)
    return render_template("admin/add_vendor.html",message=msg)

@app.route('/retrivepassword',methods = ['POST', 'GET'])
def retrivepassword():
    msg = ""
    if request.method == 'POST':
        msg = guest_controller.forgot2(request)
        print(msg)
    return render_template("guest/forgot2.html",message=msg)


@app.route('/admin-home')
def admin_home():
    return render_template("admin_home.html")



@app.route('/user_home')
def user_home():  
    return render_template("user_home.html")




@app.route('/pending_staffs')
def pending_staffs():  
    data = admin_controller.getPendingStaffs()
    return render_template("admin/new_staffs.html", employeeList = list(data))


@app.route('/approve_users')
def approve_users():
    admin_controller.approveUser(request)
    data = admin_controller.getPendingUsers()
    return render_template("approve_user.html", employeeList = list(data))


@app.route('/active_staffs')
def active_staffs():  
    data = admin_controller.getActiveStaffs()
    return render_template("admin/active_staffs.html", employeeList = list(data))

@app.route('/view_complaints')
def view_complaints():  
    data = admin_controller.getComplaints()
    return render_template("admin/View_complaints.html", employeeList = list(data))


@app.route('/suspend_staff')
def suspend_staffs():
    admin_controller.suspendStaff(request)
    data = admin_controller.getActiveStaffs()
    return render_template("admin/active_staffs.html", employeeList = list(data))

@app.route('/suspended_staffs')
def suspended_staffs():
    data = admin_controller.getSuspendedStaff()
    return render_template("admin/suspended_staffs.html", employeeList = list(data))

@app.route('/DisplayEssayDetails')
def DisplayEssayDetails():
    data = user_controller.getEssayDetails()
    return render_template("view_essaydetails.html", employeeList = list(data))

@app.route('/essay_management',methods = ['POST', 'GET'])
def essay_management():
    msg=""
    if request.method == 'POST':
        msg = admin_controller.addEssayDetails(request)
   
    return render_template("essay_management.html",message=msg) 










@app.route('/sitevisit_management',methods = ['POST', 'GET'])
def sitevisit_management():
    if request.method == 'POST':
        msg = user_controller.addSiteVisitDetails(request)
    data = user_controller.getUserDetails()
    data1 = user_controller.getItemNames()
    return render_template("user/Request_site_visit.html", catagoryList = list(data), catagoryList1 = list(data1))

@app.route('/customer_feedback',methods = ['POST', 'GET'])
def customer_feedback():
    global session
    if request.method == 'POST':
        #print(session["user"])
        msg = user_controller.addFeedback(request)
    data1 = user_controller.getItemNames()
    return render_template("user/Customer_feedback.html",  catagoryList1 = list(data1))

@app.route('/view_essay_management',methods = ['POST', 'GET'])
def view_essay_management():
    global session
    # session["id"]=request.args.get("id")
    if request.method == 'GET':
        #print(session["user"])
        id= user_controller.makeEssay(request)
    #data1 = uidser_controller.getItemDetails()
    return render_template("essay_upload.html", essayid=id)




@app.route('/subcatagory_managment',methods = ['POST', 'GET'])
def sub_catagory():
    if request.method == 'POST':
        msg = admin_controller.addSubCatagory(request)
    sub_cats = admin_controller.getSubCatagory() 
    cats = admin_controller.getCatagory()
    return render_template("admin/sub_catagory_management.html", cats = list(cats), sub_cats = list(sub_cats))

@app.route('/essay_upload',methods = ['POST', 'GET'])
def essay_upload():
    if request.method == 'POST':
        msg = user_controller.addEssay(request)
    
    if request.method == 'POST':
        # check if the post request has the file part
        
        file = request.files['filename']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            print("inside file")
            #UPLOAD_FOLDER = 'static/Upload_images'
           # UPLOAD_FOLDER = './static/Upload_images/'
            #app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            filename = secure_filename(file.filename)
            print("saving file", filename, os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("saved")
            #redirect(url_for('uploaded_file',filename=filename))
 
    return render_template("essay_upload.html")

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#def allowed_file(filename):
    #return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file:
#             filename = secure_filename(file.filename)
#             print("saving file")
#             file.save(os.path.join(UPLOAD_FOLDER, filename))
#             return redirect(url_for('uploaded_file',filename=filename))



@app.route('/order_status',methods = ['POST', 'GET'])
def order_status():
    global session
    itemname = ""
    print("Sessions", session)
    username=""#session['customer']
    g_total=0
    itemid=request.form["itemid"]
    quantity = request.form["quantity"]
    paymentmode=request.form["mode"]
    saddress=request.form["shipaddress"]
    baddress=request.form["billaddress"]
    uprice=request.form["uprice"]
    q=int(quantity)
    u=int(uprice)
    g_total+=q*u
    today_date=date.today()
    
    print(username)
    query = f"insert into order(item_id,user_id,quantity,total,paymentmode,shipping_address,billing_address,date) values ('{itemid}','{username}','{itemname}','{quantity}','{g_total}','{paymentmode}',,'{saddress}',,'{baddress}','{today_date}')"
    # return excuteCommit(query), itemname
    return render_template("user/order_sucssess.html")

@app.route('/cart_management',methods = ['POST', 'GET'])
def cart_management():
    global session
    
    if request.method == 'GET':
        print("inside addcart")
        return("item added to cart successfully")
        msg= user_controller.addCart(request)
        
    
    return render_template("user/View_item_details.html" ,message=msg)

@app.route('/DisplayMyCart')
def DisplayMyCart():
    data = user_controller.getCartDetails(request)
    return render_template("user/View_cart.html", employeeList = list(data))

@app.route('/DisplayMarketingDetails')
def DisplayMarketingDetails():
    data = user_controller.getMarketingDetails(request)
    return render_template("user/View_marketingDetails.html", employeeList = list(data))


@app.route('/marketing',methods = ['POST', 'GET'])
def marketing():
    msg = ""
    if request.method == 'POST':
        msg = staff_controller.addMarketingDetils(request)
    return render_template("staff/marketing.html",message=msg)

@app.route('/testresult',methods = ['POST', 'GET'])
def testresult():
   
    msg = ""
    if request.method == 'POST':
        msg = staff_controller.addTestResult(request)
    return render_template("staff/Test_result.html",message=msg,designation='Pathologist')


if __name__ =='__main__':  
    app.run(debug = True)  