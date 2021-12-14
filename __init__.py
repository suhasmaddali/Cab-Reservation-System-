import os
from dash import Dash
from flask import Flask,render_template,request,redirect,url_for
import json
import pandas as pd
# from werkzeug.wsgi import DispatcherMiddleware
# from werkzeug.security import generate_password_hash
from flaskext.mysql import MySQL
from ast import literal_eval


def get_from_searchdata(data):
    tupl=data[0]
    return(tupl[0],tupl[1],tupl[2],tupl[4],tupl[5],tupl[6])

def get_zip_from_address(address):
    spl=address.split(" ")
    if(len(spl)>2):
        return spl[-2]
    elif(len(spl)==0):
        return ""
    else:
        return spl[0]




    
       

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'Manthan@123'
    app.config['MYSQL_DATABASE_DB'] = 'cab_reservation'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql = MySQL()

    mysql.init_app(app)
    conn = mysql.connect()
    cursor = conn.cursor()

    
    
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
 

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
 

    # a simple page that says hello
    @app.route('/home')
    def login():
        cid="1"
        
        uname=(request.args.get("uname"))
        pwd=request.args.get("pwd")
        # hash_pwd = generate_password_hash(pwd)
        cursor.callproc('check_new_username',("manthan",uname,pwd))
        data = cursor.fetchall()
        if len(data)==0:
            # conn.commit()
            print("User created successfully !")
        else:
            cid=data[0][0]
            uname=data[0][1]

            print("user already there")

        return render_template('index.html',result={"cid":cid,"uname":uname})
    @app.route("/afterlogin")
    def afterloginhome():
        return render_template('index.html')

 
    @app.route("/about")
    def about():
        return render_template("index-1.html")
    @app.route("/cars")
    def cars():
        return render_template("index-2.html")
    @app.route("/services")
    def services():
        return render_template("index-3.html")
    @app.route("/contacts")
    def contacts():
        return render_template("index-4.html")
    @app.route('/')
    def signup():
        return render_template("signin.html")
    @app.route("/hello")
    def signnewuser():
        return render_template("newuser.html")
    @app.route("/search",methods=["GET","POST"])
    def search():
        
            data=literal_eval(request.args.get("booking"))
            

            return render_template("search.html",result={"cid":data["cid"],"uname":data["uname"]})
    @app.route("/showavdr/<customer_id>")
    def drv(customer_id):
        cursor.callproc("get_latest_search_customer",(customer_id))
        data=cursor.fetchall()
        search_id,source_add,dest_add,customer_id,szip,dzip=get_from_searchdata(data)
        response="12"
        flag=0
        cursor.callproc("zip_changes",(szip,dzip,response,flag))
        results=(cursor.fetchall())
        flag=results[0][0]
        response=results[0][1]
        print(response)
        cursor.execute('SELECT * FROM zips_serviced')
        data=cursor.fetchall()
        # df = pd.DataFrame(data.fetchall())
        # df.columns = data.keys()

        if(flag==0):
            return render_template("service_not_avail.html",response=response,avail_zips=data)
        else:
            return render_template("book.html")
    @app.route("/showdrivers",methods=["GET","POST"])
    def drivers():
        if(request.method=="POST"):
            source_location=request.form["loc"]
            destination_location=request.form["loc2"]
            customer_id=(request.form["cid"])
            user_name=(request.form["uname"])
            source_zip=request.form["pc"]
            dest_zip=request.form["pc2"]
           
            if(not source_zip.isnumeric()):
                source_zip=None
            if(not dest_zip.isnumeric()):
                dest_zip=None
            cursor.callproc('insert_new_search',(source_location,destination_location,customer_id,source_zip,dest_zip))
            conn.commit()



            return "/showavdr"+"/"+customer_id

    @app.route("/driver_availability/<driver_id>")
    def availability(driver_id):
        
        cursor.callproc("get_drivers_details",(driver_id))
        available_data=cursor.fetchall()
        carnames,car_plates=[],[]#
        for data in available_data:
            carnames.append(data[0])
            car_plates.append(data[1])
        
        cursor.execute('SELECT * FROM zips_serviced')
        zipcodes=cursor.fetchall()
        zips=[]#
        for zipcode in zipcodes:
            zips.append(zipcode[0])
        print(car_plates)

        return render_template("driver_availability.html",carnames=carnames,car_plates=car_plates,zips=zips,driver_id=driver_id)

   


   

  
  
       
    @app.route("/driveravailpage/<driver_id>")
    def afteravailabilitytoggled(driver_id):
        print(driver_id)
        av=request.args.get("Availability")
        zip=request.args.get("zip")
        carplate=request.args.get("name")
        # result=cursor.execute("toggle_driver_availability",((driver_id),(carplate),(zip),(av)))
        cursor.execute("SELECT toggle_driver_availability(%s,%s,%s,%s); ", (str(driver_id),str(carplate),str(zip),str(av) ))
        conn.commit()
        print(cursor.fetchall())
        return "hi"
    @app.route("/feedback")
    def feedback():
        return render_template("feedback_form.html")
    @app.route("/onsubmit_feedback",methods=["GET","POST"])
    def feedback2():
        rating=(request.form.keys())[0]
        message=request.form["commentText"]
    
        # rating=4
        driver_id=2
        # message="It was a fantastic ride"
        trip_id=4
        feedback_id=2
 
   
        try:     
                 conn.autocommit=False
                #  sql1 = """insert into feedback(message,rating,trip_id) values("genuinely good trip",5,3);"""
                 cursor.execute("""insert into feedback(message,rating,trip_id) values(%s,%s,%s);""",(message,"3",trip_id))
                 sql2="""select cab_reservation.get_new_driver_rating(%s, %s);"""
                 cursor.execute(sql2,(driver_id,rating))
                 new_rating=cursor.fetchall()[0][0]
                 sql3="""update driver set driver_rating=(%s) where driver_id=(%s)"""
                 cursor.execute(sql3,(new_rating,driver_id))
                 conn.commit()
                 conn.autocommit=True
        except:
            conn.rollback()
        # (feedback_id, message,rating,trip_id )


        return "hi"



    return app

