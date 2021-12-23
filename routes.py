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

    @app.route('/home')
    def login():
        
        uname=(request.args.get("uname"))
        pwd=request.args.get("pwd")
        cursor.callproc('check_username',(uname,pwd))
        data = cursor.fetchall()
        print(data)
        if data[0][0] == 1 :
        #     #conn.commit()
            print("user checked successfully !")
            return render_template('index.html')
        elif (data[0][0] ==2):
            print("incorrect credentials!")
            return render_template('signin.html',response="incorrect_credentials")
        else:
            print("Please sign up")
            return render_template('signup1.html')