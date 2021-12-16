import os
from dash import Dash
from flask import Flask,render_template,request,redirect,url_for
import json
import pandas as pd
import plotly.express as px
import plotly
from wordcloud import WordCloud
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import datetime
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
    # @app.route('/home')
    # def login():
    #     cid="1"
    #     uname=(request.args.get("uname"))
    #     pwd=request.args.get("pwd")
    #     cursor.execute("""select customer_id from customer where user_name=(%s) """,(uname))
    #     cid=cursor.fetchall()[0][0]
    #     print(cid)
       
    #     # hash_pwd = generate_password_hash(pwd)
    #     cursor.callproc('check_new_username',("manthan",uname,pwd))
    #     data = cursor.fetchall()
    #     if len(data)==0:
    #         # conn.commit()
    #         print("User created successfully !")
    #     else:
    #         cid=data[0][0]
    #         uname=data[0][1]

    #         print("user already there")
    @app.route('/') ## Login page. First page for the users
    def signup():
        return render_template("signin.html",response="")
    @app.route('/home') 
    def login():
        uname=(request.args.get("uname"))
        pwd=request.args.get("pwd")
        cursor.callproc('check_username',(uname,pwd))
        data = cursor.fetchall()
        print(data)
        if data[0][0] == 1 :
            cursor.execute("""select customer_id from customer where user_name=(%s) """,(uname))
            cid=cursor.fetchall()[0][0]
            print("user checked successfully !")
            return render_template('index.html',result={"cid":cid,"uname":uname})
        elif (data[0][0] ==2):
            print("incorrect credentials!")
            return render_template('signin.html',response="incorrect_credentials")
        else:
            print("Please sign up")
            return render_template('signup1.html')

    @app.route("/signup1")
    def signup_info():
        return render_template('signup1.html')
    
    @app.route("/onsignupclick")
    def signupcheck():
        uname=(request.args.get("uname"))
        pwd=request.args.get("psw")
        p_name = request.args.get("p_name")
        p_address = request.args.get("p_address")
        cursor.callproc('csp_1',(p_name,uname,pwd,p_address))
        data = cursor.fetchall()
        print(data)
        if (len(data) == 0):
            conn.commit()
            print("pass")
            return render_template("signin.html")
        else:
            # conn.commit()
            print("fail")
            return render_template("signup1.html")
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
        
    @app.route("/adminlogpage")
    def adminlogpage():
        return render_template("adminlogin.html")

    @app.route("/driverlogpage")
    def driverlogpage():
        return render_template("driverlogin.html")
    
    @app.route('/onadminlogin')
    def adminlogin():
        
        uname=(request.args.get("uname"))
        pwd=request.args.get("pwd")
        cursor.callproc('check_admin',(uname,pwd))
        data = cursor.fetchall()
        print("data lenth",data,len(data))
        
        if data[0][0] ==  1:
            #conn.commit()
            print("admin checked successfully !")
            return render_template('index2.html') 
        elif data[0][0] == 2:
            print("incorrect credentials")
            return render_template('signin.html')
        else:
            print("unsucessful attempt")
            return render_template('signin.html')

        #return render_template('index2.html')

    @app.route('/ondriverlogin')
    def driverlogin():
        
        uname=(request.args.get("uname"))
        pwd=request.args.get("pwd")
        cursor.callproc('check_driver',(uname,pwd))
        data = cursor.fetchall()
        print("data lenth",data,len(data))
        
        if data[0][0]== 1:
            #conn.commit()
            print("driver checked successfully !")
            return redirect("/driver_availability/"+uname) 
        elif data[0][0] == 2:
            print("Incorrect credentails")
            return render_template('signin.html') 
        else:
            print("unsucessful attempt")
            return render_template('signup1.html')
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
    
    @app.route('/chart1')
    def chart1():

        cursor.execute('SELECT * FROM trip_time_view')
        
        table_rows = cursor.fetchall()

        df = pd.DataFrame(table_rows,columns = ["trip_id","start_time","est_arrival_time","act_end_time"])
        print(df.columns)
        print(df.head())

        df["start_time"] = pd.to_datetime(df["start_time"])
        df["est_end_time"] = pd.to_datetime(df["est_arrival_time"])
        df["act_trip_time"] = pd.to_datetime(df["act_end_time"])-pd.to_datetime(df["start_time"])
        df["est_trip_time"] = pd.to_datetime(df["est_end_time"])-pd.to_datetime(df["start_time"])
        df["act_trip_time_int"] = df["act_trip_time"].dt.total_seconds().div(60).astype(int)
        df["est_trip_time_int"] = df["est_trip_time"].dt.total_seconds().div(60).astype(int)
        df["trip_diff"] = df["act_trip_time_int"] - df["est_trip_time_int"]   
        trip_diff_df  = df.resample('H', on='start_time').agg({'trip_diff':'mean'}).replace(np.nan,0)
        trip_diff_df = trip_diff_df.reset_index()
        plot = px.line(trip_diff_df, x="start_time", y="trip_diff", labels = {"start_time":"Hour of the Day","trip_diff":"Time in Mins"},title='Time Difference',)
             
        # final_df = df.resample('H', on='start_time').agg({'est_trip_time':'mean', 'act_trip_time':'mean'}).replace(np.nan,"00:00:00")
        # plot = go.Figure(data=[go.Scatter(
        # x = final_df.index,
        # y = final_df['est_trip_time'],
        # stackgroup='one'),
        #                go.Scatter(
        # x = final_df.index,
        # y = final_df['act_trip_time'],
        # stackgroup='one')])

        graphJSON = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)
        header="Arrival Time Difference"
        description = """
        Difference between Actual Trip Time and Estimated Trip Time .
        """
        cursor.execute('SELECT * FROM feedback_view')
        
        table_rows = cursor.fetchall()
        df2 = pd.DataFrame(table_rows,columns = ["feedback_message"])
        df2 = df2.dropna()
        input_text = df2.feedback_message
        print(df2.head())

        #plt.subplots(figsize = (8,8))

        wordcloud = WordCloud (
                    background_color = 'white',
                    width = 1408,
                    height = 450
                        ).generate(' '.join(input_text))
        wordcloud.to_file("/home/manthan/idmp/cab_reservation/crs/static/images/wordcloud.png")
        header6 = "Feedbacks"
        description6 = """We take feedbacks given seriously """
        #plt.imshow(wordcloud) # image show
        #plt.axis('off') # to off the axis of x and y
        #plt.savefig('/Users/simrangoindani/Documents/parent_cab/crs/static/images/Plotly-World_Cloud.png')   

        cursor.execute('SELECT * FROM sample_avail')
        
        table_rows = cursor.fetchall()
        book_drive_df = pd.DataFrame(table_rows,columns = ["HOD","driver_avai","Bookings_made"])
        book_mean = book_drive_df.groupby("HOD",as_index = False).agg({"driver_avai":"mean","Bookings_made":"mean"})
        book_mean.apply(np.floor,inplace = True)


        import plotly.graph_objects as ge        
        fig3= ge.Figure(data=[
        ge.Bar(name='Number of Bookings', x=book_mean["HOD"], y=book_mean["Bookings_made"],),
            ge.Bar(name='Available Drivers', x=book_mean["HOD"], y=book_mean["driver_avai"])])

        # Change the bar mode
        fig3.update_layout(barmode='group')
        fig3.update_layout(title_text='Bookings vs Drivers Available', title_x=0.5,xaxis_title="Hour of the Day",
        yaxis_title="Average count",)
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
        header3="Availability of Drivers vs Bookings made at every hour of the day"
        description3 = """
        This shows us the ratio of availablity of drivers whether we should focus on making more drivers available at specific intervals in the day.
        """

        # fig4 = go.Figure()
        # fig4 = go.Figure(go.Indicator(
        # mode = "gauge+number+delta",
        # value = 200,
        # title = {'text': "Averge Revenue"},
        # delta = {'reference': 300},
        # domain = {'x': [0, 1], 'y': [0, 1]}
        # ))

        # fig4 = go.Figure(go.Indicator(
        # mode = "number+delta",
        # value = 400,
        # number = {'prefix': "$"},
        # #delta = {'position': "top", 'reference': 320},
        # domain = {'x': [0, 1], 'y': [0, 1]}))

        # fig4.update_layout(paper_bgcolor = "lightgray")
        cursor.execute('SELECT * FROM fare_table')
        fare_table = cursor.fetchall()
        fare_df = pd.DataFrame(fare_table,columns = {"fare_id","fare"})
        print(fare_df.head(2))
        
        revenue = sum(fare_df["fare"])
        ride_count = fare_df["fare_id"].count()
        #print("revenue",revenue)

        cursor.execute('SELECT * FROM customer_count')
        cc_table = cursor.fetchall()
        cc_df = pd.DataFrame(cc_table,columns = {"cust_id"})
        customer_count = len(pd.unique(cc_df['cust_id']))

        cursor.execute('SELECT * FROM driver_count')
        dc_table = cursor.fetchall()
        dc_df = pd.DataFrame(dc_table,columns = {"driver_id"})
        driver_count = len(pd.unique(dc_df['driver_id']))
        fig4 = go.Figure()

        fig4.add_trace(go.Indicator(
        mode = "number",
        value = revenue*0.4,
        number = {'prefix': "$"},
        domain = {'x': [0, 0.5], 'y': [0, 0.5]},
        title = {"text": "Total Revenue<br>"}))
        #delta = {'reference': 400, 'relative': True, 'position' : "top"}))

        fig4.add_trace(go.Indicator(
        mode = "number",
        value = ride_count,
        #delta = {'reference': 400, 'relative': True},
        domain = {'x': [0, 0.5], 'y': [0.5, 1]},
        title = {"text": "Total Rides<br>"}))

        fig4.add_trace(go.Indicator(
        mode = "number",
        value = driver_count,
        #delta = {'reference': 400, 'relative': True},
        domain = {'x': [0.6, 1], 'y': [0, 0.5]},
        title = {"text": "Total Drivers<br>"}))

        fig4.add_trace(go.Indicator(
        mode = "number",
        value = customer_count,
        #delta = {'reference': 400, 'relative': True},
        domain = {'x': [0.6, 1], 'y': [0.5, 1]},
        title = {"text": "Total Customers<br>"}))

        # fig4.add_trace(go.Indicator(
        # mode = "number+delta",
        # value = 450,
        # title = {"text": "Accounts<br><span style='font-size:0.8em;color:gray'>Subtitle</span><br><span style='font-size:0.8em;color:gray'>Subsubtitle</span>"},
        # delta = {'reference': 400, 'relative': True},
        # domain = {'x': [0.6, 1], 'y': [0, 1]}))


        
        graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
        header4="4th graph"
        description4 = """
        Total.
        """

        Rev_df = pd.DataFrame({"DOW":["Sun","Mon","Wed","Fri","Mon","Tue","Wed","Thu","Thu"],"Revenue":[30,50,100,40,20,170,90,120,45]})
        Rev_df.groupby("DOW",as_index = False)["Revenue"].mean()


        fig5 = px.pie(Rev_df, values='Revenue', names='DOW', title='Distribution of Average Revenue')
        graphJSON5 = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
        header5="Distribution of average revenue "
        description5 = """
        Piechart shows revenue generated per day.
        """
        

        return render_template('notdash.html', graphJSON=graphJSON, graphJSON5=graphJSON5,graphJSON4=graphJSON4,graphJSON3=graphJSON3,
        header=header,header5=header5,header4=header4,header3=header3,header6=header6,
        description=description ,description3=description3,description4=description4,description5 = description5,description6=description6)

        # return render_template('notdash.html', graphJSON=graphJSON, header=header,description=description)




    @app.route('/plotlydash')

    def notdash():

        df = pd.DataFrame({'trip_id': [1,2,3,4],
        'start_time': ["2021-12-11 07:00:00","2021-12-11 08:00:00","2021-12-11 12:00:00","2021-12-11 14:00:00"],
        'est_end_time': ["2021-12-11 09:00:00","2021-12-11 08:40:00","2021-12-11 13:20:00","2021-12-11 14:10:00"],
        'act_end_time':["2021-12-11 09:10:00","2021-12-11 08:50:00","2021-12-11 13:10:00","2021-12-11 14:05:00"]})   
        fig = px.bar(df, x='Fruit', y='Amount', color='City', barmode='group')   
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)  

        return render_template('notdash.html', graphJSON=graphJSON)






 
    

    @app.route("/search",methods=["GET","POST"]) ## gets to the search page
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

        if(flag==0):
            return render_template("service_not_avail.html",response=response,avail_zips=data)
        else:
            cursor.execute("""select distance,estimated_time_minutes from distance_between where from_zip=(%s) and to_zip=(%s)""",(szip,dzip))
            result=cursor.fetchall()
            distance=result[0][0]
            estimated_time_minutes=result[0][1]
            return render_template("book.html",response={"cid":customer_id,"source_zip":szip,"destination_zip":dzip,"distance":distance,"estimated_time_minutes":estimated_time_minutes})
    @app.route("/cabarriving",methods=["GET","POST"])
    def cab_arriving():
        print(request.form)
        cursor.execute("""select find_nearest_driver(%s,%s)""",(request.form["szip"],request.form["Comfort"]))
        result=cursor.fetchall()[0][0]
        if(result==0):
            return "There are currently no drivers available for these specifications. Plese try later"
        else:
            driver_id=result[0]
            number_plate=result[1:]
            cursor.execute("""select * from driver where driver_id=(%s)""",(driver_id))
            drd=cursor.fetchall()[0]
            name=drd[1]
            number=drd[2]
            rating=drd[4]


            cursor.execute("""select car_name from driver_cars where driver_id=(%s) and number_plate=(%s) """,(driver_id,number_plate))
            car_name=cursor.fetchall()[0][0]
            print(car_name)
            cursor.execute("""update driver_cars set availability=0 where driver_id=(%s) and number_plate=(%s) """,(driver_id,number_plate))
            conn.commit()
            cursor.execute("""select distance,estimated_time_minutes from distance_between where to_zip=(%s) and from_zip=(%s)""",(request.form["dzip"],request.form["szip"]))
            results=cursor.fetchall()[0]
            distance=results[0]
            et_trip=results[1]
            time_trip=float(et_trip)+float(request.form["estimated_time_minutes"])
            est_arrival_time=datetime.datetime.now()+datetime.timedelta(minutes=time_trip)
    


            


            return render_template("cab_arriving.html",response={"drname":name,"number":number,"rating":rating,"driver_id":driver_id,"carname":car_name,"ETA":request.form["estimated_time_minutes"],"customer_id":request.form["cid"],"trip_distance":distance,"et_trip":et_trip,"number_plate":number_plate,"est_arrival_time":est_arrival_time})
    @app.route("/tripbegins",methods=["GET","POST"])
    def begintrip():
        # print(request.form)
        f=request.form
        start_time=datetime.datetime.now()
        
        return render_template("endtrip.html",response={"cid":f["cid"],"dist":f["dist"],"eat":f["est_arrival_time"],"start_time":start_time,"driver_id":f["driver_id"]})
        

    
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
        rating=list(request.form.keys())[0]
        print(rating)

        message=request.form["commentText"]
        print(message)
        # rating=5
    
        # rating=4
        driver_id=3
        # message="It was a fantastic ride"
        trip_id=5
        # feedback_id=2
 
   
        try:     
                 conn.autocommit=False
                #  sql1 = """insert into feedback(message,rating,trip_id) values("genuinely good trip",5,3);"""
                 cursor.execute("""insert into feedback(message,rating,trip_id) values(%s,%s,%s);""",(message,rating,trip_id))
                 sql2="""select cab_reservation.get_new_driver_rating(%s, %s);"""
                 cursor.execute(sql2,(driver_id,rating))
                 new_rating=cursor.fetchall()[0][0]
                 sql3="""update driver set driver_rating=(%s) where driver_id=(%s)"""
                 cursor.execute(sql3,(new_rating,driver_id))
                 conn.commit()
                 conn.autocommit=True
        except:
            conn.rollback()
        return render_template("final.html")
        # (feedback_id, message,rating,trip_id )
    @app.route("/beforefeedback",methods=["GET","POST"])
    def payment():
        f=request.form
        print(f)
        distance=f["dist"]
        eat=f["est_arrival_time"]
        driver_id=f["driver_id"]
        cid=f["cid"]
        import datetime
        end_time=datetime.datetime.now()
        # cursor.callproc("insert_trip",(distance,eat,f["start_time"],end_time,driver_id,cid,))
        
        now = datetime.datetime.now()
        hour=now.hour
        admin_id="manthanmehta"
        try:
            conn.autocommit=False
            sql1="""select cab_reservation.get_milely_rate(%s, %s,%s);"""
            cursor.execute(sql1,(hour,distance,"18"))
            charges=cursor.fetchall()[0][0]
            cursor.callproc("insert_trip",(distance,eat,f["start_time"],end_time,driver_id,cid,float(charges)*float(distance)))
            
            print(charges)
            sql2="""select cab_reservation.update_wallet_balances(%s,%s,%s,%s);"""
            cursor.execute(sql2,(driver_id,cid,admin_id,charges))
            conn.commit()
            conn.autocommit=True

        except:
            conn.rollback()

        return redirect("/feedback")

 


        

        



        



    return app

