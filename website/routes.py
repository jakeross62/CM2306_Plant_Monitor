from flask import render_template, url_for, request, redirect, flash, session
from website import app, db
from website.models import User
from website.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user
import csv

@app.route("/register",methods=['GET','POST'])
def register():
  form = RegistrationForm()
  if request.method == 'POST':
    user = User(username=form.username.data, password=form.password.data)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('registered'))
  return render_template('register.html',title='Register',form=form)

@app.route("/registered")
def registered():
  return render_template('registered.html', title='Thanks!')

@app.route("/", methods=['GET', 'POST'])
@app.route("/vitals",methods=['GET','POST'])
def login():
  form = LoginForm()
  if request.method == 'POST':
    user = User.query.filter_by(username=form.username.data).first()
    if user:
      if user.password == form.password.data:
        login_user(user)
        flash("You have been successfully logged in!")
        # Collecting data from csv and adding it to website only when user is logged in.
        vitals_data = [] #list of data displayed on the website
        #print("running")
        with open('data.csv') as csv_file:
            #print("reading")
            csv_reader = csv.reader(csv_file)
            length = sum(1 for line in csv_file)
        with open('data.csv') as csv_file:
            #print("reading")
            csv_reader = csv.reader(csv_file)
            csv_row = 0
            current_hour = -1
            temp_hour_data = [[],[],[]]
            for row in csv_reader:
                #print(row)->test statement
                #print(csv_row)->test statement
                csv_row +=1
                if row != ['Humidity (%)', 'Temperature (*C)', 'Light Intensity', 'Time']:
                    if current_hour != row[3][:2] or csv_row == length:
                        #print(current_hour)
                        #print(row[3][:2])
                        #print("hour change")#->test statement
                        if current_hour == -1:
                            #print("first element")#->test statement
                            current_hour = row[3][:2]
                        else:
                            if csv_row == length:
                                temp_hour_data[0].append(float(row[0]))
                                temp_hour_data[1].append(float(row[1]))
                                temp_hour_data[2].append(float(row[2]))
                            #print("actual hour change") #->test statement
                            temp_row = []
                            temp_row.append(round(hour_mean(temp_hour_data[0]),1))
                            temp_row.append(round(hour_mean(temp_hour_data[1]),1))
                            temp_row.append(round(hour_mean(temp_hour_data[2]),1))
                            temp_row.append(current_hour+":00")
                            vitals_data.append(temp_row)
                            temp_hour_data = [[],[],[]]
                            current_hour = row[3][:2]
                            temp_hour_data[0].append(float(row[0]))
                            temp_hour_data[1].append(float(row[1]))
                            temp_hour_data[2].append(float(row[2]))
                    else:
                        #print("adding information about hour")#->test statement
                        temp_hour_data[0].append(float(row[0]))
                        temp_hour_data[1].append(float(row[1]))
                        temp_hour_data[2].append(float(row[2]))
        print(vitals_data)
                
                    
        return render_template('vitals.html',vitals_data=vitals_data,data_graph=vitals_data)
    flash("Incorrect username or password!")
  return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
  logout_user()
  return render_template('logged_out.html', title="Thanks for checking on your plant!")

@app.route("/camera", methods=['GET','POST'])
def login1():
  form = LoginForm()
  if request.method == 'POST':
    user = User.query.filter_by(username=form.username.data).first()
    if user:
      if user.password == form.password.data:
        login_user(user)
        flash("You have been successfully logged in!")
        return render_template('camera.html')
    flash("Incorrect username or password!")
  return render_template('login.html',title='Login',form=form)

def hour_mean(data_for_hour):
    mean = 0
    try:
        return (sum(data_for_hour)/len(data_for_hour))
    except:
        return mean