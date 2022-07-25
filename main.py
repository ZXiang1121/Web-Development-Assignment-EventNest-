from flask import Flask, redirect, url_for, render_template, request, session, flash
from forms import signupForm, loginForm, forgetpw, changPw, createEvent
import shelve, Event, account
from werkzeug.utils import secure_filename
import os
from werkzeug.datastructures import CombinedMultiDict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOAD_FOLDER'] = 'static/images'

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/ticketDetails')
def ticketdetails():
    return render_template('ticketDetails.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = loginForm(request.form)
    if request.method == 'POST':
        return redirect(url_for('accountDetails'))
    return render_template('users/login.html', form=login)

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def create_user():
    signup = signupForm(request.form)
    if request.method == 'POST':

        users_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")

        user = account.Account(signup.name.data, signup.email.data, signup.password.data, signup.birthdate.data,)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        # Test codes
        users_dict = db['Users']
        user = users_dict[user.get_user_id()]
        print(user.get_name(), "was stored in storage.db successfully with user_id ==", user.get_user_id())

        db.close()

        return redirect(url_for('accountDetails'))
    return render_template('users/signup.html', form=signup)

@app.route('/forgetpw', methods=['GET', 'POST'])
def forgetpass():
    forgetpwform = forgetpw(request.form)
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('users/forgetpw.html', form=forgetpwform)



@app.route('/accountDetails')
def accountDetails():
    users_dict = {}
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('users/accountDetails.html', users_list=users_list)

@app.route('/EditAcc')
def EditAcc():
    return render_template('EditAcc.html')

@app.route('/ChangePass')
def ChangePass():
    return render_template('users/ChangePass.html', form=changPw)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



@app.route('/createEventForm', methods = ['GET', 'POST'])
def create_event():
    event_form = createEvent(CombinedMultiDict((request.files, request.form)))
    print(event_form)
    print("---")

    if request.method == 'POST' and event_form.validate():
        imageFile = event_form.event_image.data # First grab the file
        print("---")
        print("file")
        print(imageFile)
        print("---")
        savePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(imageFile.filename))
        imageFile.save(savePath) # Save the file

        events_dict = {}
        db = shelve.open('storage.db', flag='c' , writeback=True)
        try:
            events_dict = db['Events']
        except:
            print('Error in retrieving Events from storage.db')

        seat = []

        seat_plan = {}

        new_event = Event.Event(
                            event_form.event_name.data,
                            event_form.event_category.data,
                            
                            event_form.event_location.data,
                            event_form.event_date.data,
                            event_form.event_time.data,
                            event_form.event_image.data.filename,
                            event_form.event_desc.data,
                            )

        events_dict[new_event.get_event_id()] = new_event
        db['Events'] = events_dict

        db.close()

        return redirect(url_for('admin_homepage'))
    return render_template('createEventForm.html', form=event_form)


@app.route('/homeAdmin')
def admin_homepage():
    events_dict = {}
    db = shelve.open('storage.db', 'r')
    events_dict = db['Events']
    db.close()

    events_list = []
    for key in events_dict:
        event = events_dict.get(key)
        events_list.append(event)
    

    return render_template('homeAdmin.html', count=len(events_list), events_list=events_list)



if __name__ == '__main__':
    app.run(debug=True)
