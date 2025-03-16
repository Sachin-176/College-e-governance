from flask import Flask, render_template, redirect, request, url_for, g, jsonify,session
from time import time
import mysql.connector
from datetime import datetime,timedelta
import pandas as pd
from datetime import datetime
from pytz import timezone
import json
from functools import wraps







app = Flask(__name__)
app.secret_key = 'pietgoverner'
app.permanent_session_lifetime = timedelta(days=30)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            user='u525192722_egovernance',
            host='srv1138.hstgr.io',
            password='FOx:k4Kt=0',
            database='u525192722_egovernance'
        )
    return g.db

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

def execute_query(query, data=None):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(query, data)
        db.commit()

def fetch_data(query, data=None, one=False):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(query, data)
        if one:
            return cursor.fetchone()
        return cursor.fetchall()


@app.route('/hl')
@login_required

def hl():
    return """
<div class="inf" style="color:white">
Please select a teacher to see remarks
</div>




"""


@app.route('/dash')
@login_required
def dash():

    if request.method == "GET":
        pass
    if g.user =="head_admin":
     return render_template("dash.html")
    else:
        return "YOU ARE NOT ALLOWED TO ACCESS DASHBOARD !! ONLY FOR ADMINS"
@app.route('/teacher', methods=['post', 'get'])
@login_required

def teacher():

    if request.method == "POST":
        name = request.form['name']
        Subject = request.form['Subject']
        cmd = f'insert into teacher values("{name}","{Subject}")'
        execute_query(cmd)

        return redirect('teacher')

    cmd = "select * from teacher"
    tea = fetch_data(cmd)

    return render_template("teachers.html", cards=tea)


@app.before_request
def before_request():
 

    if 'user' in session:

        g.user = session['user']
    else:
        g.user = None


@app.route('/login',methods=['post','get'])
def login():
      print("CODE REACHED TILL HERE")
      if request.method == 'POST':
          
            user=request.form["user"]
            user=user.lower()
            password=request.form["password"]
            password=password.lower()
            
            cmd=f'select password,dsg from admin where username="{user}"'


            try:
            
          
                
                # execute_query(cmd)
                data=fetch_data(cmd)
                rpass=data[0][0]
                print(rpass,password)
                

                if rpass.lower()==password:
                    print("details matched")
                    print("user enetered")
                    print(user)
                    
                    session['user'] = user
                    return redirect(url_for('main'))
                else:
                    resp="dsp"
                    return render_template('login.html',resp=resp)

            

                        
                        
                    
                   
                    
            except:
                
                    resp="dsp"
                    return render_template('login.html',resp=resp)
                     

         
       
          

        
             
        
          


      return render_template("login.html")


# @app.route('/',methods=['GET', 'POST'])
# def main():
#     if g.user:
#         # session.clear()
#         return render_template("home.html",name=g.user)

    
#     return redirect(url_for('login'))


@app.route("/")
@login_required
def main(methods=['post', 'get']):
    if g.user:
        # session.clear()
        return render_template("VISIT.html",name=g.user)

    
    return redirect(url_for('login'))

    # first get all the block added till now rendered to

    # return render_template('VISIT.html')


@app.route('/home', methods=["POST", "GET"],)
@login_required

def home():
    print(g.user)
    if g.user : 
    
        if g.user =="head_admin":
            return render_template("home.html",boolean=1)
            
        
        return render_template("home.html",boolean=0)
    

    # return redirect(add)


@app.route("/add", methods=["POST", "GET"])
@login_required

def add():
    if request.method == "POST":
        teacher = "DS"
        block = "D-block"
        Day = "Th"
        Floor = 4
        periods = ["9:05:00 - 10:00:00", "10:00:00  - 10:55:00", "10:55:00 - 11:50:00", "11:50:00 - 12:45:00",
                   "12:45:00 - 1:40:00", "1:40:00 - 2:35:00", "2:35:00 - 3:30:00", "3:30:00 - 4:25:00"]
        list = request.get_json()
        print("------------------")
        print(list)
        print("------------------")

        for i in list:
            if 2 > len(str(i[1])):
                ni = "0"+str(i[1])
                room = str(Floor)+ni
                period = i[0]

           
                cmd = f'INSERT INTO tt (teacher, block, room, day, period) VALUES ("{teacher}", "{block}", "{room}", "{Day}", "{period}")'
                print(cmd)

                execute_query(cmd)
                # return "Something went wrong  please try again"

            else:
                period = i[0]

                room = str(Floor)+str(i[1])

                cmd = f'INSERT INTO tt (teacher, block, room, day, period) VALUES ("{teacher}", "{block}", "{room}", "{Day}", "{period}")'
                print(i)

                execute_query(cmd)
                # except:
                #     return "Something went wrong  please try again"

            print(teacher, block, room, Day, time)
        # cmd=f'insert into tt values({teacher},{block},)'

        return "ok"


@app.route('/block', methods=["POST", "GET"])
@login_required

def getblock():
    if request.method == "GET":
        cmd = "select bname from block"
        blockl = fetch_data(cmd)

    return render_template("block.html", cards=blockl)


@app.route('/shb', methods=["POST", "GET"])
@login_required

def shb():
    return render_template('addb.html')


@app.route('/floor', methods=["POST", "GET"])
@login_required

def getfloor():
    if request.method == "GET":
        block = request.args.get('var1')
        cmd = f"select bfloors from block where bname='{block}'"
        floors = fetch_data(cmd)
        floors = int(floors[0][0])
        Floorli = []
        for i in range(0, floors):
            i = i+1
            f = str(i)+"  - floor"
            print(Floorli)
            Floorli.append(f)
            print(i)

    return render_template("floors.html", cards=Floorli, block=block)


@app.route('/room', methods=["POST", "GET"])
@login_required

def getroom():
    if request.method == "GET":
        floors = request.args.get('var1')
        block = request.args.get('var2')
        cmd = f"select room from block where bname='{block}'"
        resp = fetch_data(cmd, one=True)
        nrooms = eval(resp[0])
        roomn = nrooms[int(floors)-1]
        roomli = []
        for i in range(0, roomn):
            i = i+1

            if 2 > len(str(i)):
                i = "0"+str(i)
                ri = str(floors)+i
                roomli.append(ri)
            else:

                ri = str(floors)+str(i)
                roomli.append(ri)

            # nrooms = (list(resp[0]))[0]
            # print(nrooms)

    return render_template("rooms.html", cards=roomli, block=block, floor=floors)


@app.route("/profile", methods=['post', 'get'])
@login_required

def profile():
    if request.method == "GET":
        india_tz = timezone('Asia/Kolkata')

        current_time_india = datetime.now(india_tz)

        print(india_tz)
        current_time_india = datetime.now(india_tz)
        print(current_time_india)
        current_day_india = current_time_india.weekday()
        weekday_name = current_time_india.strftime("%A")
        winit = weekday_name[0:2]
        floors = request.args.get('var1')
        block = request.args.get('var2')
        room = request.args.get('var3')
        # day=winit
        # d = "wedenesday"
        current_day = datetime.now()


# Extract the current day
        day = current_day.strftime('%A')
        day=day.lower()
        if day=="thursday":
            day="th"
            
        else:

          day = day[0]
          
        print(day)
        cmd = "select * from conditions"
        cnd = fetch_data(cmd)
        cmd2= f"select * from tt where block = '{block}' and room = '{room}' and day='{day}' ORDER BY period ASC"
        

        # current teacher,time,day

        def get_current_period(ctime):
            # Define the periods
            periods = [
                "9:05:00 - 10:00:00", "10:00:00 - 10:55:00", "10:55:00 - 11:50:00",
                "11:50:00 - 12:45:00", "12:45:00 - 13:40:00", "13:40:00 - 14:35:00",
                "14:35:00 - 15:30:00", "15:30:00 - 16:25:00"
            ]

            current_time = current_time_india.time()

            for i, period in enumerate(periods, start=1):
                start_time, end_time = period.split(" - ")
                start_time = datetime.strptime(start_time, "%H:%M:%S").time()
                end_time = datetime.strptime(end_time, "%H:%M:%S").time()

                if start_time <= current_time <= end_time:
                    return i

            return "Not within any period"

# Get the current time in the format HH:MM:SS
        current_time = current_time_india.strftime("%H:%M:%S")
        print(datetime.now())
        # current_time = "15:53:46"
        current_time = datetime.strptime(current_time, "%H:%M:%S").time()
        print(current_time)
        

        # Call the function with the current time
        current_period = get_current_period(current_time)
        # period=current_period
        period = current_period
        print("--------")
        print(period)
        cmd = f'select teacher,department from tt where block="{block}" and  room="{room}"  and period="{period}" and day="{day}" '
        print(cmd)
        data = fetch_data(cmd, one=True)
        data2 = fetch_data(cmd2)

        # teacher="AKM"

        if data:
            teacher = data[0]
            #  teacher=teacher[0]
            dpart = data[1]
            

            return render_template("profile.html", time=current_time, teacher=teacher, day=weekday_name, block=block, room=room, cards=cnd, dpart=dpart,data2=data2)

        return render_template("profile.html", time=current_time, teacher="No teacher", day=weekday_name, cnd=cnd, block=block, room=room,data2=data2)

        # day = currtime.strftime("%A")

        return render_template("profile.html")

    # first get all the block added till now rendered to

    return render_template("profile.html")


@app.route("/notate", methods=["POST", "GET"])
@login_required

def notate():
    india_tz = timezone('Asia/Kolkata')

    current_time_india = datetime.now(india_tz)

    current_day_india = current_time_india.weekday()
    weekday_name = current_time_india.strftime("%A")
    string = request.get_data()
    data = json.loads(string)
    teacher = data['teacher']
    print("------------")
    print(teacher)
    print("------------")

    block = data['block']
    room = data['room']
    dpart = data['dpart']
    list_with_whitespace = data['li']
    current_time = current_time_india.time()
    list_without_whitespace = [s.strip() for s in list_with_whitespace]
    # cmd=f'insert into nott values("{teacher}","{point}","{current_time}","{weekday_name}")'
    for i in list_without_whitespace:
        point = i
        cmd = f'insert into nott values("{teacher}","{point}","{current_time}","{weekday_name}","{block}","{room}","{dpart}")'
        execute_query(cmd)
    return "ok"


@app.route("/teacherm", methods=["POST", "GET"])
@login_required

def teacherm():

    # cmd="select distnict(teacher) from nott"
    cmd = """ SELECT teacher,COUNT(teacher) as count
        FROM nott 
        GROUP BY teacher 
        HAVING COUNT(teacher) > 0 """
    data = fetch_data(cmd)
    cmd = "select distinct(department) from nott"
    dpt = fetch_data(cmd)
    return render_template("teachers.html", cards=data, departs=dpt)


@app.route("/indepth")

@login_required

def indepth():

    teacher = request.args.get('var1')
    cmd = f"select  * from nott where teacher='{teacher}'"
    print(cmd)
    data = fetch_data(cmd)

    return render_template("list.html", data=data)


@app.route("/class")
@login_required

def classes():

    cmd = f"select  * from tt"
    print(cmd)
    data = fetch_data(cmd)

    return render_template("classes.html", data=data)


@app.route('/uploadexcel', methods=['POST', 'GET'])
@login_required

def upload_excel():

    # try:

        cmd = "delete from tt"
        execute_query(cmd)

        excel_file = request.files['excel']
        table_name = 'tt'
        df = pd.read_excel(excel_file)

        for _, row in df.iterrows():
            insert_query = f"""
                    INSERT INTO {table_name} ({', '.join(df.columns)})
                    VALUES ({', '.join(['%s'] * len(row))})
                """
            print(insert_query)
            execute_query(insert_query, tuple(row))
           

        print("Successfully uploaded")

        return redirect('/class',)

    # except:
    #     return redirect('/class')


if __name__ == '__main__':

    app.run(debug=True)
