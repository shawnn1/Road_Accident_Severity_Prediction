import pickle
import numpy as np
from flask import Flask,render_template,request,jsonify
import urllib.request
import urllib.parse
from twilio.rest import Client
from flask_mysqldb import MySQL
  

app = Flask(__name__)
#load the model
model=pickle.load(open("model.pkl","rb"))
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='road_accident'
mysql=MySQL(app)

def cal(ip):
    input = dict(ip)
   
    day = input['day']
    weather = input['weather']
    light = input['light']
    Type_of_collision=input['Type_of_collision']
    Number_of_vehicles_involved=input['Number_of_vehicles_involved']
    Number_of_casualties=input['Number_of_casualties']
    Vehicle_movement=input['Vehicle_movement']
    address=input['address']

    data = np.array([day,light,weather,Type_of_collision,Number_of_vehicles_involved,Number_of_casualties,Vehicle_movement])
    print (Number_of_casualties)
    
    data = data.reshape(1, -1)
    print(data)

   

    try: result = model.predict(data)
    except Exception as e: result = str(e)

    if day=='3' :
         dayy="Sunday"
    if day=='1' :
         dayy="Monday"
    if day=='5' :
         dayy="Tuesday"
    if day=='6' :
         dayy="Wednesday"  
    if day=='4' :
         dayy="Thursday" 
    if day=='0' :
         dayy="Friday"
    if day=='1' :
         dayy="Saturday"

    if weather=='2':
         weatherr="Normal"
    if weather=='4':
         weatherr="Raining"     


    if light=='3':
         lightt="Daylight"
    if light=='0':
         lightt="Darkness-lights lit"  

    if (int(Number_of_casualties)>20):
         ans="Fatal"
    elif (int(Number_of_casualties)>10 and int(Number_of_casualties)<20):
         ans="Serious" 
    else:
         ans="Slight" 
                      
                      
    cur=mysql.connection.cursor()
    cur.execute ('insert into all_predicted_data(Day,Weather,Light,Type_of_collision,Number_of_vehicles_involve,Number_of_casualities,Address,Accident_severity ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(dayy,weatherr,lightt,Type_of_collision,int(Number_of_vehicles_involved),int(Number_of_casualties),address,ans))
    mysql.connection.commit()
    cur.close()                  
     
    
    if(int(Number_of_casualties)>10 & int(Number_of_casualties)<20) :
      return str(1);
    elif(int(Number_of_casualties)>20) :
         return str(0);
    else:
      return str(result[0])  
    


   
    





@app.route('/map/', methods=['GET'])
def map():
    return render_template('map.html')
@app.route('/logout',methods=['GET'])
def logout():
      return render_template('preindex.html')
@app.route('/Home/',methods=['GET'])
def home():
     return render_template('index.html')

@app.route('/sms/', methods=['POST'])
def sms():
   SID='AC0254e62ecc58be79a4be6e74c43dc5d7'
   auth='ae694eaa5b07eb64105b63c4f3acb329'
   client = Client( SID,auth)
   message = client.messages.create(
        body='A severe accident happened',
        from_ ='+12706793367',
        to ='+8801755763136'
   )
   
   return cal(request.form)   


@app.route('/',methods=['GET'])
def hello_world():
    return render_template("preindex.html")
@app.route('/login',methods=['GET'])
def log():
     return render_template('login.html')

@app.route('/form_login',methods=['POST'])
def login():
    name1=request.form['username']
    pwd=request.form['password']
    cur=mysql.connection.cursor()
    user=cur.execute('select * from register where Name=%s and Password=%s',(name1,pwd))
    if user:
	    return render_template('index.html')
    else:
       return render_template('login.html',info='Invalid Password/name')
@app.route('/sign',methods=['GET'])
def sign():
     return render_template('sign.html')    
@app.route('/sign_in',methods=['POST'])
def signin():
    name1=request.form['username']
    pwd=request.form['password']
    email=request.form['email']
    cur=mysql.connection.cursor()
    cur.execute ('insert into register (Name,Password,Email) VALUES (%s,%s,%s)',(name1,pwd,email))
    mysql.connection.commit()
    cur.close()
    return render_template('sign.html',info='succeed')

@app.route('/visual/',methods=['GET'])
def visual():
     cur=mysql.connection.cursor()
     cur.execute('select * from all_predicted_data')
     alldata = cur.fetchall()
     return render_template('visual.html',alldata=alldata)          
@app.route('/', methods=['POST'])

def get():
    return cal(request.form)

if __name__=='__main__':
    app.run(port=3000,debug=True);