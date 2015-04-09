CS3130 Assignment 7
Janelle Montgomery

A python program that uses sqlite3 and flask. This program creates an interactive app that allows a user to access an employee database. The user will be able to search and display the database as well as add and delete users. 
The application requires a login.
username: admin
password: default

In order to run this website in terminal you will need two windows open.
Run: python3 db_flask.py
This is the main program that will direct the html template pages as well as handle interactions with the database.
Run: python3 db_mainflask.py
This will allow for a connection to the database.

The schema1.sql file contains the database table 'employees' that will be accessed on the app. The user id is not required to be entered as it is automatically incremented from the last entry :).

Most of the code that I used is referenced from the flask tutorial website.

git hub url: https://github.com/JanellePearl/cs3130_Assignment7.git
