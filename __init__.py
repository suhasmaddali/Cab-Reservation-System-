import os

from flask import Flask,render_template,request,redirect,url_for
import json
# from werkzeug.security import generate_password_hash
from flaskext.mysql import MySQL
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'Manthan@123'
    app.config['MYSQL_DATABASE_DB'] = 'cab_reservation'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
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
        
        uname=(request.args.get("uname"))
        pwd=request.args.get("pwd")
        # hash_pwd = generate_password_hash(pwd)
        cursor.callproc('check_new_username',("manthan",uname,pwd))
        data = cursor.fetchall()
        print(data)
        if len(data) is 0:
            # conn.commit()
            print("User created successfully !")
        else:
            print("user already there")

        return render_template('index.html')
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
    # @app.route("/login",methods=["POST","GET"])
    # def onclicklogin():
    #     if request.method == 'POST':
    #         user = request.form['uname']
    #         pwd=request.form["pwd"]
    #         print(user,pwd)
    #         return redirect(url_for('/home',name = user))
    #     else:
    #         user = request.args.get("uname")
            
    #         pwd=request.args.get("pwd")
    #         print(user,pwd)
    #         return redirect(url_for('/home'))

        # _name = request.form['inputName']
        # _email = request.form['inputEmail']
        # _password = request.form['inputPassword']
        # if _name and _email and _password:
        #     return json.dumps({'html':'<span>All fields good !!</span>'})
        # else:
        #     return json.dumps({'html':'<span>Enter the required fields</span>'})
    # @app.route('/signUp',methods=['POST'])
    # def signUp():
    #     _name = request.form['inputName']
    #     _email = request.form['inputEmail']
    #     _password = request.form['inputPassword']
    #     _hashed_password = generate_password_hash(_password)
        # cursor.callproc('check_new_username',(_name,_email,_hashed_password))
        # data = cursor.fetchall()
        # if len(data)==0 :
        #     conn.commit()
        #     return json.dumps({'message':'User created successfully !'})
        # else:
        #     return json.dumps({'error':str(data[0])})

       


    return app

