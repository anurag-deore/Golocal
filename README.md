# Golocal
 Flask based Web Platform for local worker to find jobs made during Hackjaipur hackathon. 
 Deployed on https://g0l0cal.herokuapp.com
 
 # Installation
 > ### Prerequisites
 > **Python 3.7** or above installed 
 
 First off, Create a virtualenv (if required)
 ```
 $ pip install virtualenv
 $ virtualenv venv
 $ .\venv\Scripts\activate
 ```
Then go on installing the *requirements.txt* file
```
$ pip install -r requirements.txt
```
Now, from the python console(shell), run following commands
```
$ python
>>> from flaskblog import db
>>> db.create_all()
>>>
```
You can ignore the ```SQLAlchemy Track Modifications Warning``` in the above step.

You will now have a **site.db**  file as your local database
Alternatively you can use mysql by altering comments  for these lines in ```flaskblog/__init__.py``` and again running the previous step
```
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/NameOfYourDatabase'
```
Exit from the python shell
```
>>> exit()
```
You're all ready to run this app using following command
```
$ python run.py
```
The project should be running on ```127.0.0.1:5000``` or ```localhost:5000```

### Hope You Enjoy this project
Feel free to raise an issue
