# Mini Project 2
## 1. Project description
This project will create an environment formed by the number of instance which the user decided to create.
The traffic sent to the instances will be managed by a load-balancer. It runs in the port 5000 

This instances will be runing a server which will allow the user to upload a photo and introduce his phone number. When the photo is uploaded the instance will upload the photo to a S3 bucket, create an entry into the database and send a message with a queue using the SQS service.

The backend will read the message, then it will download the photo from the bucket using the database entry, then it will flip it and upload again to the bucket. Finally, it will send a SMS to the user using SNS.

## 2. Parts of the project
This project has the following files:
* Create-app.sh is an script which will load all the configuration in the instances managed by the load balancer.
* Create-backend2.sh is an script which will load all the configuration in the instance which will perform the photo modification.
* create-env.sh is the script which will be run by the user to create the full environment
* destroy-env.sh is the script which will destroy the environment (It deletes all the .priv files storaged in the directory, so be careful when running it.)
* MP2.json is the policy file

In the pythonPrograms folder we will find:
* imageprocessor.py which is the software which is going to edit the photo and upload the modification to the bucket
* uploadimages.py which is the software which is going to create the server to upload the photo, persist the information into the database, upload the photo to the bucket and send a message to the imageprocessor.py

Then in the templates folder:
* imageupload.html which is the web page to upload the file.

## 3. User action
For running the create-env.sh the user can introduce the ami uploaded to the blackboard in the MP1 as a positional parameter or not introduce any ami. The rest of the parameters used by the program and which are going to be defined by the user will be asked during the program execution.

## 4. Demo video 
https://youtu.be/oGKF5CsqP3Y
