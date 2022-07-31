import os
from flask import Flask, redirect, url_for, render_template, request, session, flash
from forms import createEvent, signupForm, loginForm, forgetpw, changPw, ContactForm, FlaskForm
import shelve, Event, account, Seat
from werkzeug.utils import secure_filename
from flask_login import LoginManager


from werkzeug.datastructures import CombinedMultiDict
import pandas as pd

# admin name: admin
# admin email: admin@gmail.com
# admin pw: eventnest

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

# make account
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader

def load_user(user_id):
    return User.get(user_id)

def get_id(val, my_dict):
    for key, value in my_dict.items():
        if val == value.get_email():
            return key
    return 'None'
def get_pw(val, my_dict):
    for key, value in my_dict.items():
        if val == value.get_password():
            return key
    return 'None'
def get_name(val, my_dict):
    for key, value in my_dict.items():
        if val == value.get_password():
            return key
    return 'None'

@app.route('/login', methods=['GET', 'POST'])
def login():
    login = loginForm(request.form)

    if request.method == 'POST':
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']

        key = get_id(login.email.data, users_dict)
        key2 = get_pw(login.password.data, users_dict)

        if key == 'None' or key != key2: 
            print(key, login.email.data, users_dict) # test
            flash('Invalid login credentials', 'danger')

        elif login.email.data == 'admin@gmail.com' and login.password.data == 'eventnest':
            user = users_dict.get(key) # get( user_id )
            db.close()
            session['admin_in'] = user.get_name()
            return redirect(url_for('admin_homepage'))

        elif key == key2:
            user = users_dict.get(key) # get( user_id )
            db.close()
            session['logged_in'] = user.get_name()

            session['username'] = user.get_name()
            session['user_id'] = user.get_user_id()
            session['user_email'] = user.get_email()
            session['user_birthdate'] = user.get_birthdate()
            return redirect(url_for('accountDetails'))

    return render_template('users/login.html', form=login)

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('logged_in', None)
   return redirect(url_for('home'))

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
        
        if signup.password.data != signup.comfirmpw.data:
            flash('Passwords do not match.', 'danger')

        else:

            key = get_id(signup.email.data, users_dict)
            if key == 'None': 

                user = account.Account(signup.name.data, signup.email.data, signup.password.data, signup.birthdate.data)
                users_dict[user.get_user_id()] = user
                db['Users'] = users_dict

                # Test codes
                users_dict = db['Users']
                user = users_dict[user.get_user_id()]
                print(user.get_name(), "was stored in storage.db successfully with user_id ==", user.get_user_id())

                db.close()

                session['user_created'] = user.get_name()

                session['username'] = signup.name.data
                

                return redirect(url_for('login'))

            else:
                flash('Email is used for an existing account.', 'danger')

    return render_template('users/signup.html', form=signup)

@app.route('/forgetpw', methods=['GET', 'POST'])
def forgetpass():
    forgetpwform = forgetpw(request.form)
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('users/forgetpw.html', form=forgetpwform)

@app.route('/newpw', methods=['GET', 'POST'])
def newpass():
    newpw = changPw(request.form)
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('users/newpw.html', form=newpw)

# account made

@app.route('/accountDetails')
def accountDetails(): # how to display info of logged in user
    login = loginForm(request.form)

    users_dict = {}
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = [] # all users information
    
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('users/accountDetails.html', users_list=users_list)
    # return render_template('users/accountDetails.html')

@app.route('/EditAcc/<uuid(strict=False):id>/', methods=['GET', 'POST'])
def EditAcc(id):    
    update_user_form = signupForm(request.form)

    if request.method == 'POST':
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_name(update_user_form.name.data)
        user.set_email(update_user_form.email.data)

        db['Users'] = users_dict
        db.close()

        session['user_updated'] = user.get_name()  
        session['username'] = user.get_name()
        session['user_id'] = user.get_user_id()
        session['user_email'] = user.get_email()
        session['user_birthdate'] = user.get_birthdate()
        return redirect(url_for('accountDetails'))

    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.name.data = user.get_name()
        update_user_form.email.data = user.get_email()

        return render_template('users/EditAcc.html', form = update_user_form)

@app.route('/ChangePass/<uuid(strict=False):id>/', methods=['GET', 'POST'])
def ChangePass(id):
    changepass = changPw(request.form)

    if request.method == 'POST':
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)

        if changepass.nowpassword.data != user.get_password():
            flash('Password does not match current password.', 'danger')

        elif changepass.newpassword.data != changepass.comfirmpw.data:
            flash('New passwords do not match.', 'danger')

        else:
            user.set_password(changepass.newpassword.data)

            db['Users'] = users_dict
            db.close()

            session['user_updated'] = user.get_name()    
            return redirect(url_for('accountDetails'))

    return render_template('users/ChangePass.html', form=changepass)

    
    

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



@app.route('/createEventForm', methods = ['GET', 'POST'])
def create_event():
    # event_form = createEvent(CombinedMultiDict((request.files, request.form)))
    event_form = createEvent(CombinedMultiDict((request.files, request.form)))
    
    print(event_form)
    print("---")

    if request.method == 'POST' and event_form.validate():
        posterFile = event_form.event_poster.data # First grab the file
        seatFile = event_form.seat_image.data
        print("---")
        print("file")
        print(posterFile)
        print("---")
        print(seatFile)
        print("---")
        savePosterPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(posterFile.filename))
        posterFile.save(savePosterPath) # Save the file
        print("---")
        saveSeatPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(seatFile.filename))
        seatFile.save(saveSeatPath) # Save the file

        events_dict = {}
        db = shelve.open('storage.db', flag='c', writeback=True)
        try:
            events_dict = db['Events']
        except:
            print('Error in retrieving Events from storage.db')


        ## uuid, createdTime

        new_event = Event.Event(
                            event_form.event_name.data,
                            event_form.event_category.data,
                            event_form.event_location.data,
                            event_form.event_date.data,
                            event_form.event_time.data,
                            event_form.event_poster.data.filename,
                            event_form.seat_image.data.filename,
                            event_form.event_desc.data,
                            )
                            
        seating_plan_list = []
        for i in event_form.data['seating_plan']:
            print(i)
            seat = Seat.Seat(i['seat_type'],
                             i['seat_available'],
                             i['seat_price'])
            seating_plan_list.append(seat)
        
        new_event.set_seating_plan(seating_plan_list)



        events_dict[new_event.get_event_id()] = new_event
        db['Events'] = events_dict

        db.close()

        # return redirect(url_for('admin_homepage'))
        return redirect(url_for('submit_result'))
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
    
    print(events_list)

    return render_template('homeAdmin.html', count=len(events_list), events_list=events_list)

@app.route('/contactus', methods=["GET","POST"])
def get_contact():
    form = ContactForm()
    # here, if the request type is a POST we get the data on contat
    #forms and save them else we return the contact forms html page
    if request.method == 'POST':
        name =  request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        res = pd.DataFrame({'name':name, 'email':email, 'subject':subject ,'message':message}, index=[0])
        res.to_csv('./contactusMessage.csv')
        print("The data are saved !")
        
    else:
        return render_template('contact.html', form=form)
    
@app.route('/faq')
def faq():
   return render_template('faq.html')


@app.route('/submitResult')
def submit_result():
    events_dict = {}
    db = shelve.open('storage.db', 'r')
    events_dict = db['Events']

    db.close()

    events_list = []
    for key in events_dict:
        event = events_dict.get(key)
        events_list.append(event)

    return render_template('submitResult.html', count=len(events_list), events_list=events_list)


@app.route('/success')
def message():
   return render_template('contactusMessage.html')






@app.route('/createQn', methods=['GET', 'POST'])
def create_qn():
    create_qn_form = CreateQnForm(Form)
    if request.method == 'POST' and create_qn_form.validate():
        qn_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            qn_dict = db['Question']
        except:
            print("Error in retrieving Users from storage.db.")

        qn = Qn.Qn(create_qn_form.first_name.data,
                         create_qn_form.last_name.data,
                         create_qn_form.email.data,
                         create_qn_form.number.data,
                         create_qn_form.comments.data)

        qn_dict[qn.get_qn_id()] = qn
        db['Question'] = qn_dict

        # Test codes
        # users_dict = db['Users']
        # user = users_dict[user.get_user_id()]
        # print(user.get_first_name(), user.get_last_name(), "was stored in storage.db successfully with user_id ==", user.get_user_id())
        #
        # db.close()


        return redirect(url_for('create_qn_form'))
    return render_template('createqnpopup.html', form=create_qn_form)





if __name__ == '__main__':
    app.run(debug=True)

