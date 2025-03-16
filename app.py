from flask import Flask,render_template ,redirect,session,request,url_for,g,jsonify
from time import time,sleep
import mysql.connector 
from datetime import datetime, timedelta
import pandas as pd
import os
from datetime import datetime
from pytz import timezone
from datetime import datetime
import json
from tabulate import tabulate

# Get the current date


# Get the weekday as an integer (Monday is 0, Sunday is 6)


# Get the weekday name


india_tz = timezone('Asia/Kolkata')
current_time_india = datetime.now(india_tz)
current_day_india = current_time_india.weekday()
weekday_name = current_time_india.strftime("%A")
winit = weekday_name[0:2]

conn=mysql.connector.connect(user="u525192722_egovernance",host="srv1138.hstgr.io",password="FOx:k4Kt=0",database="u525192722_egovernance")
sql= conn.cursor()




app=Flask(__name__)



@app.route('/hl')
def hl():
    return """
Please select a teacher to see remarks




"""


@app.route('/dash')
def dash():

    if request.method=="GET":
        pass






    return render_template("dash.html")


@app.route('/teacher',methods=['post','get'])
def teacher():

    if request.method=="POST":
        name=request.form['name']
        Subject=request.form['Subject']
        cmd=f'insert into teacher values("{name}","{Subject}")'
        sql.execute(cmd)
        conn.commit()

        return redirect('teacher')


        


    cmd="select * from teacher"
    sql.execute(cmd)
    tea=sql.fetchall()


    



    return render_template("teachers.html",cards=tea)


@app.route("/")
def addb(methods=['post','get']):
    if request.method=="POST":
        # list=request.get_json()
        # print("------------------")
        # print(list)
        # print("------------------")
        pass


    # first get all the block added till now rendered to

    return render_template('VISIT.html')


@app.route('/home',methods=["POST","GET"])
def home():
    cmd=""" SELECT teacher, COUNT(teacher) as count
        FROM nott 
        GROUP BY teacher 
        HAVING COUNT(teacher) > 0;
        """
    sql.execute(cmd)
    t=sql.fetchall()
    return render_template("home.html",cards=t)


    
    # return redirect(add)

@app.route("/add",methods=["POST","GET"])
def add():
    if request.method=="POST":
        teacher="DS"
        block="D-block"
        Day="Th"
        Floor=4
        periods=["9:05:00 - 10:00:00","10:00:00  - 10:55:00","10:55:00 - 11:50:00","11:50:00 - 12:45:00","12:45:00 - 1:40:00","1:40:00 - 2:35:00","2:35:00 - 3:30:00","3:30:00 - 4:25:00"]
        list=request.get_json()
        print("------------------")
        print(list)
        print("------------------")

      
        for i  in list:
            if 2>len(str(i[1])):
                ni="0"+str(i[1])
                room=str(Floor)+ni
                period=i[0]

            # INSERT INTO tt (teacher, block, room, day, period) VALUES ("VD", "D-block", "415", "Th", "7")
            # INSERT INTO tt (teacher, block, room, day, period) VALUES ("VD", "D-block", "415", "Th", "7")
            # INSERT INTO tt (teacher, block, room, day, period) VALUES ("VD", "D-block", "415", "Th", "7")
            # INSERT INTO tt (teacher, block, room, day, period) VALUES ("VD", "D-block", "415", "Th", "7")
            # INSERT INTO tt (teacher, block, room, day, period) VALUES ("VD", "D-block", "415", "Th", "7")
            # INSERT INTO tt (teacher, block, room, day, period) VALUES ("VD", "D-block", "415", "Th", "7")
            # INSERT INTO tt (teacher, block, room, day, period) VALUES ("VD", "D-block", "415", "Th", "7")
            # INSERT INTO tt (teacher, block, room, day, period) VALUES ("VD", "D-block", "415", "Th", "7")
            # INSERT INTO tt (teacher, block, room, day, period) VALUES ("VD", "D-block", "415", "Th", "7")
            # INSERT INTO tt (teacher, block, room, day, period) VALUES ("VD", "D-block", "415", "Th", "7")

          


            
               

            #    INSERT INTO tt (teacher, block, room, day, period) VALUES ("VD", "D-block", "4", "15   ","7")

              
                cmd = f'INSERT INTO tt (teacher, block, room, day, period) VALUES ("{teacher}", "{block}", "{room}", "{Day}", "{period}")'
                print(cmd)

             
                sql.execute(cmd)
                conn.commit()
             
                # return "Something went wrong  please try again"
                
                

            else:
                period=i[0]

                room=str(Floor)+str(i[1])
                
                cmd = f'INSERT INTO tt (teacher, block, room, day, period) VALUES ("{teacher}", "{block}", "{room}", "{Day}", "{period}")'
                print(i)
               
               
                sql.execute(cmd)
                conn.commit()
                # except:
                #     return "Something went wrong  please try again"
                
            
            print(teacher,block,room,Day,time)
        # cmd=f'insert into tt values({teacher},{block},)'
        




        return "ok"
        


@app.route('/block',methods=["POST","GET"])
def getblock():
    if request.method=="GET":
        cmd="select bname from block"
        sql.execute(cmd)
        blockl=sql.fetchall()

    return render_template("block.html",cards=blockl)
        

@app.route('/shb',methods=["POST","GET"])
def shb():
    return render_template('addb.html')


@app.route('/floor',methods=["POST","GET"])
def getfloor():
    if request.method=="GET":
        block=request.args.get('var1')
        cmd=f"select bfloors from block where bname='{block}'"
        sql.execute(cmd)
        floors=sql.fetchall()
        floors=int(floors[0][0])
        Floorli=[]
        for i in range(0,floors):
            i=i+1
            f=str(i)+"  - floor"
            print(Floorli)
            Floorli.append(f)
            print(i)
      


    return render_template("floors.html",cards=Floorli,block=block)



@app.route('/room',methods=["POST","GET"])
def getroom():
    if request.method=="GET":
        floors=request.args.get('var1')
        block=request.args.get('var2')
        cmd=f"select room from block where bname='{block}'"
        sql.execute(cmd)
        resp=sql.fetchone() 
        nrooms = eval(resp[0]) 
        roomn=nrooms[int(floors)-1]
        roomli=[]
        for i in range(0,roomn):
            i=i+1

            if 2>len(str(i)):
                i="0"+str(i)
                ri=str(floors)+i
                roomli.append(ri)
            else:
              
                ri=str(floors)+str(i)
                roomli.append(ri)
            
          
           
           

        
            # nrooms = (list(resp[0]))[0]
            # print(nrooms)
        
       
      


    return render_template("rooms.html",cards=roomli,block=block,floor=floors)
        


@app.route("/profile",methods=['post','get'])
def profile():
    if request.method=="GET":
        floors=request.args.get('var1')
        block=request.args.get('var2')
        room=request.args.get('var3')
        # day=winit
        d="Friday"
        day=d[0]
        print(day)
        cmd="select * from conditions"
        sql.execute(cmd)
        cnd=sql.fetchall()

        


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
        current_time = datetime.now().strftime("%H:%M:%S")
        # current_time = "15:53:46"
        current_time = datetime.strptime(current_time, "%H:%M:%S").time()
        print(current_time)




        # Call the function with the current time
        current_period = get_current_period(current_time)
        # period=current_period
        period=current_period
        print("--------")
        print(period)
        cmd=f'select teacher,department from tt where block="{block}" and  room="{room}"  and period="{period}" and day="{day}" '
        print(cmd)
        sql.execute(cmd)
        data=sql.fetchone()
      
       
        # teacher="AKM"
       
        if data:
                 teacher=data[0]
                #  teacher=teacher[0]
                 dpart=data[1]

                 
                 return  render_template("profile.html" , time=current_time,teacher=teacher ,day=weekday_name,block=block,room=room, cards=cnd,dpart=dpart) 

        return  render_template("profile.html" , time=current_time,teacher="No teacher" ,day=weekday_name, cnd=cnd ,block=block,room=room,)





                # day = currtime.strftime("%A")
        
        
        
        
       


        
        return render_template("profile.html")

        


       

        
    # first get all the block added till now rendered to

    return render_template("profile.html")



@app.route("/notate",methods=["POST","GET"])
def notate():
    current_day_india = current_time_india.weekday()
    weekday_name = current_time_india.strftime("%A")
    string=request.get_data()
    data=json.loads(string)
    teacher=data['teacher']
    print("------------")
    print(teacher)
    print("------------")

    block=data['block']
    room=data['room']
    dpart=data['dpart']
    list_with_whitespace=data['li']
    current_time = current_time_india.time()
    list_without_whitespace = [s.strip() for s in list_with_whitespace]
    # cmd=f'insert into nott values("{teacher}","{point}","{current_time}","{weekday_name}")'
    for i in list_without_whitespace:
        point = i 
        cmd=f'insert into nott values("{teacher}","{point}","{current_time}","{weekday_name}","{block}","{room}","{dpart}")'
        sql.execute(cmd)
        conn.commit()
    return "ok"
   

@app.route("/teacherm",methods=["POST","GET"])
def teacherm():

    # cmd="select distnict(teacher) from nott"
    cmd=""" SELECT teacher,COUNT(teacher) as count
        FROM nott 
        GROUP BY teacher 
        HAVING COUNT(teacher) > 0 """
    sql.execute(cmd)
    data=sql.fetchall()
    cmd="select distinct(department) from nott"
    sql.execute(cmd)
    dpt=sql.fetchall()
    return render_template("teachers.html",cards=data,departs=dpt)
    




@app.route("/indepth")
def indepth():

    teacher = request.args.get('var1')
    cmd=f"select  * from nott where teacher='{teacher}'"
    print(cmd)
    sql.execute(cmd)
    data=sql.fetchall()
    

    return render_template("list.html",data=data)


@app.route("/class")
def classes():

   
    cmd=f"select  * from tt"
    print(cmd)
    sql.execute(cmd)
    data=sql.fetchall()
    

    return render_template("classes.html",data=data)

  

@app.route('/uploadexcel', methods=['POST','GET'])
def upload_excel():
        
    try:

            
            cmd="delete from tt"
            sql.execute(cmd)
            conn.commit()

        

            excel_file = request.files['excel']
            table_name = 'tt'
            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():
                insert_query = f"""
                    INSERT INTO {table_name} ({', '.join(df.columns)})
                    VALUES ({', '.join(['%s'] * len(row))})
                """
                sql.execute(insert_query, tuple(row))

            conn.commit()
        
            print("Successfully uploaded")

            return redirect('/class',) 
    
    except :
        return redirect('/class') 


   



if __name__ == '__main__':
   

   
    app.run(debug=True)

