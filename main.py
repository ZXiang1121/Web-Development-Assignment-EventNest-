import os
from flask import Flask, redirect, url_for, render_template, request, session, flash

# session timeout
import flask
import flask_login
import datetime

import User
from forms import createEvent, signupForm, loginForm, forgetpw, changPw, ContactForm, addOrder
import shelve, Event, account, Seat, Order, Payment
from werkzeug.utils import secure_filename
from flask_login import LoginManager

from werkzeug.datastructures import CombinedMultiDict
import pandas as pd
import smtplib
from email.message import EmailMessage
# admin name: admin
# admin email: admin@gmail.com
# admin pw: eventnest

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOAD_FOLDER'] = 'static/images'

@app.before_request
def before_request():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=30)
    flask.session.modified = True
    flask.g.user = flask_login.current_user

@app.route('/')
def home():
    events_dict = {}
    db = shelve.open('storage.db', 'c')
    events_dict = db['Events']

    db.close()

    events_list = []
    for key in events_dict:
        event = events_dict.get(key)
        events_list.append(event)

    return render_template('home.html', count=len(events_list), events_list=events_list)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

@app.route('/ticketDetails/<uuid(strict=False):id>', methods=['GET', 'POST'])
def ticket_details(id):

    events_dict = {}
    db = shelve.open('storage.db', 'r')
    events_dict = db['Events']
    db.close()

    events_list = []
    for key in events_dict:
        event = events_dict.get(key)
        events_list.append(event)

    for page in events_list:
        if page.get_event_id() == id:
            retrieve_event = page

    add_order_form = addOrder(request.form)
    add_order_form.order_price.choices = [(i.get_seat_price(), i.get_seat_type())
                                            for i in retrieve_event.get_seating_plan()]

    if request.method == 'POST' and add_order_form.validate():

        orders_dict = {}
        db = shelve.open('storage.db', 'c')
        try:
            orders_dict = db['Orders']
        except:
            print('Error in retrieving Orders from storage.db')
    
        dc = {v:k for k, v in add_order_form.order_price.choices}
        key_list = list(dc.keys())
        value_list = list(dc.values())
        position = value_list.index(int(add_order_form.order_price.data))

        # print(add_order_form.order_price.)
        new_order = Order.Order(
                            retrieve_event.get_event_id(),
                            retrieve_event.get_event_name(),
                            retrieve_event.get_event_category(),
                            retrieve_event.get_event_location(),
                            retrieve_event.get_event_poster(),
                            retrieve_event.get_seat_image(),
                            retrieve_event.get_event_date(),
                            retrieve_event.get_event_time(),
                            retrieve_event.get_event_desc(),
                            key_list[position],
                            add_order_form.order_price.data,
                            add_order_form.order_quantity.data,
                            retrieve_event.get_seating_plan()
                            )
        
        orders_dict[new_order.get_order_id()] = new_order
        db['Orders'] = orders_dict

        db.close()


        return redirect(url_for('cart_page'))
    return render_template('ticketDetails.html', event=retrieve_event, form=add_order_form)



@app.route('/updateTicketDetails/<uuid(strict=False):id>/', methods=['GET', 'POST'])
def update_ticket_details(id):

    update_order_form = addOrder(request.form)
    
    if request.method == 'POST':
    # if request.method == 'POST' :
        db = shelve.open('storage.db', 'w')
        orders_dict = db['Orders']


        orders_list = []
        for key in orders_dict:
            order = orders_dict.get(key)
            orders_list.append(order)
        
        # print(orders_list)

        for page in orders_list:
            if page.get_order_id() == id:
                # print(page.get_order_id())
                retrieve_order = page

        order = orders_dict.get(id)

        update_order_form.order_price.choices = [(i.get_seat_price(), i.get_seat_type())
                                        for i in retrieve_order.get_order_seating_plan()]
        
        dc = {v:k for k, v in update_order_form.order_price.choices}
        key_list = list(dc.keys())
        value_list = list(dc.values())
        position = value_list.index(int(update_order_form.order_price.data))

        order.set_order_seat_type(key_list[position])
        order.set_order_seat_price(update_order_form.order_price.data)
        order.set_order_quantity(update_order_form.order_quantity.data)

        db['Orders'] = orders_dict
        db.close()

        return(redirect(url_for('cart_page')))

    else:

        orders_dict = {}
        db = shelve.open('storage.db', 'r')
        orders_dict = db['Orders']
        db.close()

        orders_list = []
        for key in orders_dict:
            order = orders_dict.get(key)
            orders_list.append(order)

        for page in orders_list:
            if page.get_order_id() == id:
                retrieve_order = page

        update_order_form.order_price.choices = [(i.get_seat_price(), i.get_seat_type())
                                        for i in retrieve_order.get_order_seating_plan()]
        
        dc = {v:k for k, v in update_order_form.order_price.choices}
        key_list = list(dc.keys())
        value_list = list(dc.values())
        
        update_order_form.order_price.data = order.get_order_seat_price()
        update_order_form.order_quantity.data = order.get_order_quantity()

    return render_template('updateTicketDetails.html', order=retrieve_order, form=update_order_form)



@app.route('/cart')
def cart_page():
    orders_dict = {}
    db = shelve.open('storage.db', 'r')
    orders_dict = db['Orders']
    # print(orders_dict)
    db.close()
    

    orders_list = []
    for key in orders_dict:
        order = orders_dict.get(key)
        orders_list.append(order)
    # print(orders_list)

    store_order_price = []
    for i in orders_list:
        store_order_price.append(i.order_cost(i.get_order_seat_price(), i.get_order_quantity()))

    total_cost = "{:.2f}".format(sum(store_order_price))


    return render_template('cart.html', count=len(orders_list), orders=orders_list, payable= total_cost)

@app.route('/clearCart/<uuid(strict=False):id>/')
def clear_cart(id):

    orders_dict = {}
    db = shelve.open('storage.db', 'r')
    orders_dict = db['Orders']
    db.close()

    orders_list = []
    for key in orders_dict:
        order = orders_dict.get(key)
        orders_list.append(order)

    payments_dict = {}
    db = shelve.open('storage.db', 'c')

    try:
        payments_dict = db['Payments']
    except:
        print('Error in retrieving Events from storage.db')
    
    new_payment = Payment.Payment(
        orders_list
    )

    db = shelve.open('storage.db', 'w')
    db['Orders'] = {}

    payments_dict[new_payment.get_payment_id()] = new_payment
    db['Payment'] = payments_dict


    users_dict = {}
    db = shelve.open('storage.db', 'w')
    users_dict = db['Users']

    user = users_dict.get(id)
    user.set_cart_item(orders_list)
    user.set_payment(new_payment)
    print(user.set_payment(new_payment))

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('home'))


@app.route('/deleteOrder/<uuid(strict=False):id>/', methods=['GET', 'POST'])
def delete_order(id):
    orders_dict = {}
    db = shelve.open('storage.db', 'w')
    orders_dict = db['Orders']

    orders_dict.pop(id)

    db['Orders'] = orders_dict
    db.close()

    return redirect(url_for('cart_page'))


# zowie
# login
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
            # print(key, login.email.data, users_dict) # test
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
            return redirect(url_for('accountDetails', id = user.get_user_id()))

    return render_template('users/login.html', form=login)

# make account
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
                # print(user.get_name(), "was stored in storage.db successfully with user_id ==", user.get_user_id())

                db.close()

                session['user_created'] = user.get_name()

                session['username'] = signup.name.data
                

                return redirect(url_for('login'))

            else:
                flash('Email is used for an existing account.', 'danger')

    return render_template('users/signup.html', form=signup)


# reset password

@app.route('/forgetpw', methods=['GET', 'POST'])
def forgetpass():
    forgetpwform = forgetpw(request.form)
    if request.method == 'POST':
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']

        key = get_id(forgetpwform.email.data, users_dict)

        if key == 'None': 
            flash('Email does not have an account', 'danger')
        
        else:
            sender_email = 'eventnest1@gmail.com'
            sender_pw = 'tenroviygfhwacpo'

            msg = EmailMessage()
            msg['Subject'] = 'Reset EventNest password'
            msg['From'] = sender_email
            msg['To'] = forgetpwform.email.data

            msg.set_content('Click the link to reset your password. http://127.0.0.1:5000{}'.format(url_for('newpass', id = key)))


            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()


                smtp.login(sender_email, sender_pw)

                smtp.send_message(msg)
            
            return redirect(url_for('login'))
    return render_template('users/forgetpw.html', form=forgetpwform)

@app.route('/newpw/<uuid(strict=False):id>/', methods=['GET', 'POST'])
def newpass(id):
    newpw = changPw(request.form)
    if request.method == 'POST':
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)

        if newpw.newpassword.data != newpw.comfirmpw.data:
            flash('Passwords do not match.', 'danger')

        else:
            
            user.set_password(newpw.newpassword.data)

            db['Users'] = users_dict
            db.close()

            session['user_updated'] = user.get_name()    
            return redirect(url_for('login'))

    return render_template('users/newpw.html', form=newpw)

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('user_id', None)
   return redirect(url_for('home'))

@app.route('/deleteacc/<uuid(strict=False):id>/')
def deleteacc(id):
    session.pop('user_id', None)
   
    users_dict = {}
    db = shelve.open('storage.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()
    return redirect(url_for('home'))


# account made
@app.route('/profile')
def profile():
    return render_template('users/profile.html')

@app.route('/accountDetails')
def accountDetails():
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
    
    # print(event_form)
    # print("---")

    if request.method == 'POST' and event_form.validate():
        posterFile = event_form.event_poster.data # First grab the file
        seatFile = event_form.seat_image.data

        savePosterPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(posterFile.filename))
        posterFile.save(savePosterPath) # Save the file

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

            seat = Seat.Seat(i['seat_type'],
                             i['seat_available'],
                             i['seat_price'])
            seating_plan_list.append(seat)
        
        new_event.set_seating_plan(seating_plan_list)



        events_dict[new_event.get_event_id()] = new_event
        db['Events'] = events_dict

        db.close()

        # return redirect(url_for('admin_homepage'))
        return redirect(url_for('admin_homepage'))
    return render_template('createEventForm.html', form=event_form)


@app.route('/updateEventForm/<uuid(strict=False):id>/', methods = ['GET', 'POST'])
def update_event(id):
    update_event_form = createEvent(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and update_event_form.validate():
        posterFile = update_event_form.event_poster.data # First grab the file
        seatFile = update_event_form.seat_image.data

        savePosterPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(posterFile.filename))
        posterFile.save(savePosterPath) # Save the file

        saveSeatPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(seatFile.filename))
        seatFile.save(saveSeatPath) # Save the file

        
        db = shelve.open('storage.db', 'w')
        events_dict = db['Events']

        event = events_dict.get(id)
        event.set_event_name(update_event_form.event_name.data)
        event.set_event_category(update_event_form.event_category.data)
        event.set_event_location(update_event_form.event_location.data)
        event.set_event_date(update_event_form.event_date.data)
        event.set_event_poster(update_event_form.event_poster.data.filename)
        event.set_seat_image(update_event_form.seat_image.data.filename)
        event.set_event_desc(update_event_form.event_desc.data)

        seating_plan_list = []
        for i in update_event_form.data['seating_plan']:
            seat = Seat.Seat(i['seat_type'],
                             i['seat_available'],
                             i['seat_price'])
            seating_plan_list.append(seat)
        
        event.set_seating_plan(seating_plan_list)

        
        db['Events'] = events_dict
        db.close()



        return redirect(url_for('admin_homepage'))
    else:

        events_dict = {}
        db = shelve.open('storage.db', 'r')
        events_dict = db['Events']
        db.close()

        event = events_dict.get(id)
        
        update_event_form.event_name.data = event.get_event_name()
        update_event_form.event_category.data = event.get_event_category()
        update_event_form.event_location.data = event.get_event_location()
        update_event_form.event_date.data = event.get_event_date()
        update_event_form.event_time.data = event.get_event_time()
        update_event_form.event_poster.data = event.get_event_poster()
        update_event_form.seat_image.data = event.get_seat_image()
        update_event_form.event_desc.data = event.get_event_desc()
        update_event_form.seating_plan = event.get_seating_plan()

        return render_template('updateEventForm.html', form=update_event_form)

@app.route('/deleteEvent/<uuid(strict=False):id>/', methods=['GET', 'POST'])
def delete_event(id):
    events_dict = {}
    db = shelve.open('storage.db', 'w')
    events_dict = db['Events']

    events_dict.pop(id)

    db['Events'] = events_dict
    db.close()

    return redirect(url_for('admin_homepage'))

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
    users_dict = {}
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']

    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    for user in users_list:
        print(user.get_email())
        for i in user.get_cart_item():
            for n in i:
                print(n.get_order_name())
            # subtotal = i.order_cost(i.get_order_seat_price(), i.get_order_quantity())
            
 

    return render_template('submitResult.html', count=len(users_list), users_list=users_list)





@app.route('/success')
def message():
   return render_template('contactusMessage.html')




@app.route('/createUser', methods=['GET', 'POST'])
def create_qn():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")

        user = User.User(create_user_form.first_name.data,
                         create_user_form.last_name.data,
                         create_user_form.gender.data,
                         create_user_form.membership.data,
                         create_user_form.remarks.data)

        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict


        return redirect(url_for('retrieve_users'))
    return render_template('createUser.html', form=create_user_form)


@app.route('/retrieveUsers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)


    return render_template('retrieveUsers.html', count=len(users_list),users_list=users_list)

@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_gender(update_user_form.gender.data)
        user.set_membership(update_user_form.membership.data)
        user.set_remarks(update_user_form.remarks.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.gender.data = user.get_gender()
        update_user_form.membership.data = user.get_membership()
        update_user_form.remarks.data = user.get_remarks()

        return render_template('updateUser.html', form=update_user_form)

@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('storage.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('retrieve_users'))

if __name__ == '__main__':
    app.run(debug=True)

