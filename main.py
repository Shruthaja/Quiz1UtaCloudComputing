from flask import Flask,render_template
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

@app.route('/')
def hello_world():
    print(cursor)
    return render_template("index.html")

def upload(file,name):
    account_url="DefaultEndpointsProtocol=https;AccountName=shruthaja;AccountKey=FvxC1NCWJQuBHKf77+JJaniZDHYUsBzqjy9H2o2o4INHFJRAXUTl6E3VB+2wXX3SsjFsMy5Vpm/R+ASto6SosQ==;EndpointSuffix=core.windows.net"
    blob_account_client = BlobServiceClient.from_connection_string(account_url)
    blob_client=blob_account_client.get_blob_client("quiz1",name+".jpg")
    blob_client.upload_blob(file,overwrite=True)
    return "https://shruthaja.blob.core.windows.net/assignment1/"+name+".jpg"

if __name__ == '__main__':
    app.run(debug=True)
