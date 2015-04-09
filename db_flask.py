#cs3130 Assignment 7
#Janelle Montgomery

#Creating an app version of the EMS database that we made previously in assignment 1
#This will implement flask as well as creating my own database using sqlite3
#A lot of the ideas I have implemented are from the flask tutorial
#link:http://flask.pocoo.org/docs/0.10/tutorial/


#ALL the imports
import sqlite3 
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
abort, render_template, flash


#load the configuration
DATABASE= 'employeeDB.db'
DEBUG=True
SECRET_KEY='development key'
USERNAME='admin'
PASSWORD='default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

#For setting up the database connection, works with db_mainflask.py
def init_db():
    with closing(connect_db()) as db: # name the connection db
        with app.open_resource('schema1.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

#This makes it so the startup page is directed to the login page
@app.route('/')
def index():
    return redirect(url_for('login'))

#after login the user is directed to the menu
@app.route('/menu')
def menu():
    session['logged_in'] = True
    return render_template('menu.html')


#to display the entire employee database
@app.route('/display')
def display_emp():
    if not session.get('logged_in'):
        abort(401)
    
    cur = g.db.execute('select user_id,user_name,user_last,user_dep FROM employees') #performs a db query
    employees = [dict(user_id=row[0],user_name=row[1],user_last=row[2],user_dep=row[3]) for row in cur.fetchall()] #displays
    return render_template('display_emp.html',employees=employees)

#to add an employee to the database
@app.route('/add', methods=['GET', 'POST'])
def add_emp():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'GET':
        return render_template('add_emp.html')#creates the webpage
    else:
        g.db.execute('insert into employees (user_name,user_last,user_dep) values (?,?,?)',   #runs a query to insert
               [request.form['user_name'],request.form['user_last'],request.form['user_dep']])
    
        g.db.commit()
        flash('New employee was sucessfully posted')
        return redirect(url_for('add_emp'))

#to delete an employee from the database
@app.route('/delete', methods=['GET', 'POST'])
def delete_emp():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'GET':
        return render_template('delete_emp.html') #creates the webpage
    else:
        #runs query
        cur = g.db.execute('SELECT user_name,user_last,user_dep FROM employees WHERE user_id=(?)', [request.form['user_id']])
        try:
            employee = cur.fetchall()
            flash("Employee removed")
            g.db.execute('delete FROM employees WHERE user_id=(?)',[request.form['user_id']])#deltes user
            g.db.commit()
            return redirect(url_for('delete_emp'))
        except:
            flash("Employee does not exist")
            return redirect(url_for('delete_emp'))

#to search for an employee   
@app.route('/search', methods=['GET', 'POST'])
def search_emp():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'GET':
        return render_template('search_emp.html') #creates the webpage
    else:
        cur = g.db.execute('SELECT user_name,user_last,user_dep FROM employees WHERE user_id=(?)', [request.form['user_id']])
        try:
            employee = cur.fetchall()
            flash(employee)
            return redirect(url_for('search_emp'))
        except:
            flash('Employee does not exist')
            return redirect(url_for('search_emp'))


#to allow the user to login
@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method  == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('menu'))
    return render_template('login.html', error=error)

#to allow the user to logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

      
if __name__ == '__main__':
    app.debug = True #allows for auto update on terminal
    app.run(port=2000) #changes default port to 2000         
                                                            
    


    
    

    
                           
    
