import boto3
from flask import Flask, render_template, request
import mysql.connector
import os
import time
import sys
app = Flask(__name__)
os.mkdir('uploads')

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

sqs = boto3.client('sqs', region_name='us-west-2')
client = boto3.client('rds', region_name='us-west-2')
bucket = boto3.client('s3',region_name='us-west-2')
db_url = client.describe_db_instances(DBInstanceIdentifier='mp2dbinstance')[
    'DBInstances'][0]['Endpoint']['Address']


def create_database():
    cnx = mysql.connector.connect(
        user='pjusue', password='mp2pjusue', host=db_url)
    cursor = cnx.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS MP2")
    cursor.close()
    cnx.close()


def create_datatable():
    cnx = mysql.connector.connect(
        user='pjusue', password='mp2pjusue', host=db_url, database='MP2')
    cursor = cnx.cursor()
    cursor.execute(
"CREATE TABLE IF NOT EXISTS MP2Data (id INT PRIMARY KEY AUTO_INCREMENT, FILENAME VARCHAR(200) NOT NULL,PHONE_NUMBER VARCHAR(200) NOT NULL, S3URL VARCHAR(255) NOT NULL, time VARCHAR(255) NOT NULL)")
    cnx.commit()
    cursor.close()
    cnx.close()


def insert_data(url,name,phone):
    cnx = mysql.connector.connect(
        user='pjusue', password='mp2pjusue', host=db_url, database='MP2')
    cursor = cnx.cursor()
    print(url)
    print(time.strftime('%Y-%m-%d-%H:%M:%S'))
    cursor.execute("INSERT INTO MP2Data (FILENAME,PHONE_NUMBER,S3URL,time) VALUES('"+name+"', '"+phone+"', '"+url.replace(' ','+')+"', '"+time.strftime('%Y-%m-%d-%H:%M:%S')+"')")
    id=cursor.lastrowid
    cnx.commit()
    cursor.close() 
    cnx.close()
    return id


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        image = request.files['file']
        phone = request.form['text']
        f = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(f)
        create_database()
        create_datatable()
        bucket.upload_file(f, 'pjfimages-bucket', image.filename)
        url = 'https://s3-us-west-2.amazonaws.com/pjfimages-bucket/'+image.filename
        id=insert_data(url,image.filename,phone)
        queue_url = sqs.get_queue_url(QueueName='MP2queue')['QueueUrl']
        sqs.send_message(QueueUrl=queue_url, MessageBody=(str(id)))

    return render_template('imageupload.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
