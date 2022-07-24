from flask import Flask, redirect, url_for, render_template, request, session, flash
from forms import signupForm, loginForm, forgetpw, changPw, createEvent
import shelve, Event

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/ticketdetails')
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

@app.route('/signup', methods=['GET', 'POST'])
def create_user():
    signup = signupForm(request.form)
    if request.method == 'POST':
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
    return render_template('users/accountDetails.html')

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

    

    return render_template('homeAdmin.html')



if __name__ == '__main__':
    app.run(debug=True)
