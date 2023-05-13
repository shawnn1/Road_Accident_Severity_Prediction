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
   
    day = input['day'][0]
    weather = input['weather'][0]
    light = input['light'][0]
    Type_of_collision=input['Type_of_collision'][0]
    Number_of_vehicles_involved=input['Number_of_vehicles_involved'][0]
    Number_of_casualties=input['Number_of_casualties'][0]
    Vehicle_movement=input['Vehicle_movement'][0]

    data = np.array([day,light,weather,Type_of_collision,Number_of_vehicles_involved,Number_of_casualties,Vehicle_movement])
    print (data)
    
    data = data.reshape(1, -1)

    x = np.array([1, 3.73, 3, 0.69, 125, 4, 1, 1, 1, 1, 30]).reshape(1, -1)

    try: result = model.predict(data)
    except Exception as e: result = str(e)

    return str(result[0])





@app.route('/map/', methods=['GET'])
def visual():
    return render_template('map.html')
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

@app.route('/form_login',methods=['POST','GET'])
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
    cur=mysql.connection.cursor()
    cur.execute ('insert into register (Name,Password,Email) VALUES (%s,%s,%s)',(name1,pwd,'123'))
    mysql.connection.commit()
    cur.close()
    return render_template('sign.html',info='succeed')
     
     
@app.route('/', methods=['POST'])

def get():
    return cal(request.form)

if __name__=='__main__':
    app.run(port=3000,debug=True);