# templates/register.html

from flask import Flask, request, render_template,session,flash
from datetime import datetime
import os
import sqlite3 as sql
from listdb import *
import pyodbc      
import pandas as pd
from flask import render_template, redirect, request    

app = Flask(__name__)
#Bootstrap(app)
app = Flask(__name__)   
# creating connection Object which will contain SQL Server Connection    
connection = pyodbc.connect('Driver={SQL Server};Server=grp40finalproject.database.windows.net;Database=cloudfinalproject;uid=hemanth;pwd=Riddleapt@302')# Creating Cursor    
    
cursor = connection.cursor()    
cursor.execute("SELECT TOP(10000) H.HSHD_NUM,BASKET_NUM,PURCHASE_,P.PRODUCT_NUM,DEPARTMENT,COMMODITY FROM [dbo].[households] h inner join [dbo].[temptran] t on h.HSHD_NUM = t.HSHD_NUM  inner join [dbo].[products] p on t.PRODUCT_NUM = p.PRODUCT_NUM order by h.HSHD_NUM")    
s = "<input type=\"text\" id=\"myInput\" onkeyup=\"myFunction()\" placeholder=\"Search for product num..\" title=\"Type in product num\"><table class=\"sortable\" id = \"myTable\"> <tr> <th>H.HSHD_NUM</th> <th>BASKET_NUM </th>  <th>PURCHASE</th>  <th>P.PRODUCT_NUM</th> <th>DEPARTMENT</th> <th>COMMODITY</th> </tr>"   
for row in cursor:    
    s = s + "<tr>"    
    for x in row:    
        s = s + "<td>" + str(x) + "</td>"    
    s = s + "</tr>"    
connection.close()  

app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


# Database
cnctn = pyodbc.connect('Driver={SQL Server};Server=grp40finalproject.database.windows.net;Database=cloudfinalproject;uid=hemanth;pwd=Riddleapt@302')

mycursor = cnctn.cursor()
@app.route('/')
def hello_world():
    return render_template('register.html')

@app.route('/registerNav/', methods=['GET','POST'])
def registerLink():
    return render_template('register.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    username=request.form["username"]
    password=request.form["password"] 
    firstname=request.form["firstname"]
    lastname=request.form["lastname"]
    email=request.form["email"]
    di = {'username':username, 'password':password,'firstname':firstname, 'lastname':lastname,'email':email}
    addRec(di)
    return render_template('login.html')

@app.route('/loginNav/', methods=['GET','POST'])
def loginNav():
    return render_template('login.html')

@app.route("/upload/", methods=['GET','POST'])
def uploadFiles():
      print('here')
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
           parseCSV(file_path)
          # save the file
      return render_template('uploadedNav.html')
def parseCSV(filePath):
      # CVS Column Names
      col_names = ['BASKET_NUM','HSHD_NUM','PURCHASE_','PRODUCT_NUM','SPEND','UNITS','STORE_R','WEEK_NUM','YEAR']
      # Use Pandas to parse the CSV file
      csvData = pd.read_csv(filePath,names=col_names, header=None)
      mycursor.execute('TRUNCATE table temptran')
      # Loop through the Rows
      for i,row in csvData.iterrows():
             sql = "INSERT INTO temptran (BASKET_NUM,HSHD_NUM,PURCHASE_,PRODUCT_NUM,SPEND,UNITS,STORE_R,WEEK_NUM,YEAR) VALUES (?,?,?,?,?,?,?,?,?)"
           #  value = (row['PRODUCT_NUM'],row['DEPARTMENT'],row['COMMODITY'],row['BRAND_TY'],row['NATURAL_ORGANIC_FLAG'])
             mycursor.execute(sql,row['BASKET_NUM'],row['HSHD_NUM'],row['PURCHASE_'],row['PRODUCT_NUM'],row['SPEND'],row['UNITS'],row['STORE_R'],row['WEEK_NUM'],row['YEAR'])
             #mydb.commit()
             print(i,row['BASKET_NUM'],row['HSHD_NUM'],row['PURCHASE_'],row['PRODUCT_NUM'],row['SPEND'],row['UNITS'],row['STORE_R'],row['WEEK_NUM'],row['YEAR'])
      cnctn.close()   

@app.route('/login/', methods=['GET', 'POST'])
def login():
    username = str(request.form['username'])
    password = str(request.form['password'])
    if validate(username,password):
        return render_template('index.html')
        #<html><head><script>function myFunction(){var l,a,m,t,n,e,y;l=document.getElementById('myInput');a=l.value.toUpperCase();m=document.getElementById('myTable');t=m.getElementsByTagName('tr');for(e=0;e<t.length;e++){n=t[e].getElementsByTagName('td')[0];if(n){y=n.textContent||n.innerText;if(y.toUpperCase().indexOf(a)>-1){t[e].style.display=''}else{t[e].style.display='none'}}}};</script><script src=\"https://www.kryogenix.org/code/browser/sorttable/sorttable.js\"></script></head><body>" + s + "</body></html>" 
    return render_template('invlogin.html')
@app.route('/viewdata/', methods=['GET', 'POST'])
def viewdata():
    return "<html><head><script>function myFunction(){var l,a,m,t,n,e,y;l=document.getElementById('myInput');a=l.value.toUpperCase();m=document.getElementById('myTable');t=m.getElementsByTagName('tr');for(e=0;e<t.length;e++){n=t[e].getElementsByTagName('td')[0];if(n){y=n.textContent||n.innerText;if(y.toUpperCase().indexOf(a)>-1){t[e].style.display=''}else{t[e].style.display='none'}}}};</script><script src=\"https://www.kryogenix.org/code/browser/sorttable/sorttable.js\"></script></head><body>" + s + "</body></html>"
@app.route('/visualize/', methods=['GET', 'POST'])
def visualize():
    return render_template('visualize.html')
if __name__ == '__main__':
 # app.secret_key = os.urandom(12)
    app.run()
