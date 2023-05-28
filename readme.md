## Install API
Prerequirements:
Python3  
Node 

## Set up python environment
```bash
$ python3 -m venv env
In seperate terminal window run the command below which needs to run to run local env
$ source env/bin/activate
```
## Use requirements to install dependencies
```bash
From the terminal window where *env* is running
$ pip install -r requirements.txt
```
## start the app
```bash
$ python3 app.py
```
## endpoints:
##### localhost:5000/api/shoe/{id} <development server>
  Caveat need to remove s3 connection first
##### localhost:5000/api/box/{id} 
##### localhost:5000/api/custom/0?sole=000000&swoosh=FFFFFF&back=000000&body=FFFFFF&top=000000&toe=FFFFFF
