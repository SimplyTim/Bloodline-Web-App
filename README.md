[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/SimplyTim/Bloodline-Web-App) 

# Bloodline Web Application
A Progressive Web Application which serves to essentially sensitize and encourage users to donate blood through user-friendly interface. The project is split into two github repositories consisting of the front end and back end respectively. The project was created using the JAM (Javascript API Markup) stack with the front end application being built with angular 9.1.1 and the back end application server with flask 1.0.2. This is the back end portion of a blood donation web application that uses RESTful API to obtain data and generate operations on that data. 

### Features of The Application

* The single-page website will host and present all the information necessary to a donor in an organized manner so that they can be knowledgeable of the process they possibly may partake in. 

* The application will allow users to view the blood donation centres within their vicinity.

* Users will be able to schedule an appointment with a chosen centre. They would be allowed to edit that appointment before the arrival date. The operations which a user will be allowed to perform on an appointment after its creation will include the ability to view, edit, or delete the appointment. 

* Hosts will be able to manage the appointments scheduled with the centre that they are employed in. This will include the ability to accept or reject an appointment in a given scenario. 

* A user of the application will be able to register, login,  and view his account information.

## Architecture
![arcitecture img](https://github.com/SimplyTim/Bloodline-Web-App/blob/master/WhatsApp%20Image%202020-05-12%20at%208.22.36%20PM.jpeg?raw=true)
The architecture of the Web Application is a JAM stack approach and requests the web services of this application server, GoogleMaps API,SQL Alchemy and Gunicorn. The front end was build using Angular.


## Requirements
* jinja2==2.11.2
* click==7.1.1
* Flask==1.0.2
* Flask-Cors==3.0.8
* Flask-JWT==0.3.2
* Flask-SQLAlchemy==2.4.0
* Flask-WTF==0.14.3
* itsdangerous==1.1.0
* PyJWT==1.4.2
* pylint-flask-sqlalchemy==0.2.0
* SQLAlchemy==1.3.15
* Werkzeug==1.0.0
* WTForms==2.2.1
* MarkupSafe==1.1.1
* gunicorn==20.0.4
* psycopg2==2.8.5

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
