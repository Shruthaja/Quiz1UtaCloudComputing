from flask import Flask, render_template, request
import pyodbc
from azure.storage.blob import BlobClient, BlobServiceClient

server = 'assignmentservershruthaja.database.windows.net'
database = 'Quiz1'
username = 'shruthaja'
password = 'mattu4-12'
driver = '{ODBC Driver 17 for SQL Server}'
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = conn.cursor()
app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def hello_world():
    row=0
    res=""
    if request.method == "POST":
        row=request.form["rowno"]
        query="Select * from dbo.q1c where row=?"
        cursor.execute(query,row)
        res=cursor.fetchall()
    return render_template("index.html",res=res)

@app.route('/seat',methods=['GET', 'POST'])
def seat():
    seatres=""
    seatletterres=""
    allres=""
    if request.method == "POST":
        seatstart=request.form['start']
        seatend=request.form['end']
        seatletter=request.form['seatletter']
        if((seatstart and seatend !="null") and seatletter=="null"):
            query = "Select * from dbo.q1c where row between ? and ?"
            cursor.execute(query, seatstart,seatend)
            seatres = cursor.fetchall()
            return render_template("index.html",seatres=seatres)
        elif(seatletter!="null" and ( seatstart and seatend =="null")):
            query = "Select * from dbo.q1c where seat=?"
            cursor.execute(query, seatletter)
            seatletterres = cursor.fetchall()
            return render_template("index.html",seatletterres=seatletterres)
        else:
            query = "Select * from dbo.q1c where row between ? and ? and seat=?"
            cursor.execute(query, seatstart, seatend,seatletter)
            allres = cursor.fetchall()
            return render_template("index.html",allres=allres)
    return render_template("index.html")

@app.route('/page2.html',methods=['GET', 'POST'])
def page2():
    res=""
    if request.method == "POST":
        name=request.form['uname']
        row=request.form['urow']
        seat=request.form['useat']
        pic=request.files['upic']
        notes=request.form['unotes']
        query="insert into dbo.q1c values(?,?,?,?,?)"
        cursor.execute(query,name,row,seat,upload(pic,name),notes)
        cursor.commit()
        query = "Select * from dbo.q1c where name=?"
        cursor.execute(query,name)
        res=cursor.fetchall()
    return render_template("page2.html",res=res)

@app.route('/delete',methods=['GET', 'POST'])
def delpage():
    res=""
    name=""
    if request.method == "POST":
        name=request.form['delname']
        query="delete from dbo.q1c where name=?"
        cursor.execute(query,name)
        cursor.commit()
    return render_template("page2.html",delres="Deleted : "+name)

def upload(file,name):
    account_url="DefaultEndpointsProtocol=https;AccountName=shruthaja;AccountKey=FvxC1NCWJQuBHKf77+JJaniZDHYUsBzqjy9H2o2o4INHFJRAXUTl6E3VB+2wXX3SsjFsMy5Vpm/R+ASto6SosQ==;EndpointSuffix=core.windows.net"
    blob_account_client = BlobServiceClient.from_connection_string(account_url)
    blob_client=blob_account_client.get_blob_client("quiz1",name+".jpg")
    blob_client.upload_blob(file,overwrite=True)
    return "https://shruthaja.blob.core.windows.net/quiz1/"+name+".jpg"

if __name__ == '__main__':
    app.run(debug=True)
