[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/SimplyTim/Bloodline-Web-App) 

# Bloodline Web Application
A Progressive Web Application which serves to essentially sensitize and encourage users to donate blood. This is the back end portion of a blood donation web application that uses RESTful API to obtain data and generate operations on that data.

## Requirements
jinja2==2.11.2
click==7.1.1
Flask==1.0.2
Flask-Cors==3.0.8
Flask-JWT==0.3.2
Flask-SQLAlchemy==2.4.0
Flask-WTF==0.14.3
itsdangerous==1.1.0
PyJWT==1.4.2
pylint-flask-sqlalchemy==0.2.0
SQLAlchemy==1.3.15
Werkzeug==1.0.0
WTForms==2.2.1
MarkupSafe==1.1.1
gunicorn==20.0.4
psycopg2==2.8.5

## Installation (Deploying on heroku)
#### Prepare the App
Clone the webapp to have a local version that you can deploy
```
$ heroku create
```
When you create an app, a git remote (called heroku) is also created and associated with your local git repository.

Deploy the code
```
$ git push heroku master
```
You can visit the app URL with 
```
$ heroku open
```



## Creators
* [akeelhenry](https://github.com/akeelhenry)
* [kumar100966](https://github.com/kumar100966)
* [SimplyTim](https://github.com/SimplyTim)
* [Romario12c](https://github.com/Romario12c)


## Front End Repo
[Project Bloodline Front End](https://github.com/kumar100966/BloodLine)
