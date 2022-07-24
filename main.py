from flask import Flask, redirect, url_for, render_template, request, session, flash
from forms import signupForm, loginForm, forgetpw, changPw, createEvent
import shelve, event, account

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'


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
    create_event_form = createEvent(request.form)
    if request.method == 'POST' and create_event_form.validate():
        events_dict = {}
        db = shelve.open('storage.db', 'c')
        try:
            events_dict = db['Events']
        except:
            print('Error in retrieving Events from storage.db')

        event = Event.Event(
                            create_event_form.event_name.data,
                            create_event_form.event_category.data,
                            create_event_form.event_location.data,
                            create_event_form.event_date.data,
                            create_event_form.event_time.data,
                            create_event_form.event_image.data,
                            create_event_form.event_desc.data,
                            )
        
        events_dict[event.get_event_id()] = event
        db['Events'] = events_dict

        db.close()

        return redirect(url_for('homeAdmin'))
    return render_template('createEventForm.html', form=create_event_form)


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
