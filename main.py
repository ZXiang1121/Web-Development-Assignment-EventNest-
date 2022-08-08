import os
from flask import Flask, redirect, url_for, render_template, request, session, flash

import Question

from forms import createEvent, signupForm, loginForm, forgetpw, changPw, CreateQnForm
import shelve, Event, account, Seat

from forms import createEvent, signupForm, loginForm, forgetpw, changPw,  addOrder
import shelve, Event, account, Seat, Order

from werkzeug.utils import secure_filename
from flask_login import LoginManager
from werkzeug.datastructures import CombinedMultiDict
import pandas as pdpy

# admin name: admin
# admin email: admin@gmail.com
# admin pw: eventnest

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOAD_FOLDER'] = 'static/images'


@app.route('/')
def home():
    events_dict = {}
    db = shelve.open('storage.db', 'r')
    events_dict = db['Events']

    db.close()

    events_list = []
    for key in events_dict:
        event = events_dict.get(key)
        events_list.append(event)

    return render_template('home.html', count=len(events_list), events_list=events_list)


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
        
        print(orders_list)

        for page in orders_list:
            if page.get_order_id() == id:
                print(page.get_order_id())
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


@app.route('/deleteOrder/<uuid(strict=False):id>/', methods=['GET', 'POST'])
def delete_order(id):
    orders_dict = {}
    db = shelve.open('storage.db', 'w')
    orders_dict = db['Orders']

    orders_dict.pop(id)

    db['Orders'] = orders_dict
    db.close()

    return redirect(url_for('cart_page'))



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


# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# Rawtbhik
@app.route('/createQn', methods=['GET', 'POST'])
def create_qn():
    create_qn_form = CreateQnForm(request.form)
    if request.method == 'POST' and create_qn_form.validate():
        qns_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            qns_dict = db['Questions']
        except:
            print("Error in retrieving Users from storage.db.")

        qn = Question.Question(create_qn_form.name.data,
                         create_qn_form.email.data,
                         create_qn_form.gender.data,
                         create_qn_form.subject.data,
                         create_qn_form.remarks.data,
                         create_qn_form.answers.data)

        qns_dict[qn.get_qn_id()] = qn
        db['Questions'] = qns_dict


        return redirect(url_for('retrieve'))
    return render_template('createQn.html', form=create_qn_form)





@app.route('/retrieveqns')
def retrieve_qns():
    qns_dict = {}
    db = shelve.open('storage.db', 'r')
    qns_dict = db['Questions']
    db.close()

    qns_list = []
    for key in qns_dict:
        qn = qns_dict.get(key)
        qns_list.append(qn)
        
    return render_template('retrieveQns.html', count=len(qns_list),qns_list=qns_list)


# @app.route('/updateQn/<int:id>/', methods=['GET', 'POST'])
# def create_ans():
#     create_ans_form = CreateQnForm(request.form)
#     if request.method == 'POST' and create_ans_form.validate():
#         qns_dict = {}
#         db = shelve.open('storage.db', 'c')
#         try:
#             qns_dict = db['Questions']
#         except:
#             print("Error in retrieving Users from storage.db.")

#         ans = Question.Question(create_ans_form.name.data)
        
#         qns_dict[ans.get_qn_id()] = ans
#         db['Questions'] = qns_dict
        
        
def update_qn(id):
    update_qn_form = CreateQnForm(request.form)
    if request.method == 'POST' and update_qn_form.validate():
        qns_dict = {}
        db = shelve.open('storage.db', 'w')
        qns_dict = db['Questions']

        qn = qns_dict.get(id)
        qn.set_name(update_qn_form.name.data)
        qn.set_email(update_qn_form.email.data)
        qn.set_gender(update_qn_form.gender.data)
        qn.set_subject(update_qn_form.subject.data)
        qn.set_remarks(update_qn_form.remarks.data)
        qn.set_answers(update_qn_form.answers.data)
        
        

        db['Questions'] = qns_dict
        db.close()

        return redirect(url_for('retrieve_qns'))
    else:
        qns_dict = {}
        db = shelve.open('storage.db', 'r')
        qns_dict = db['Questions']
        db.close()

        qn = qns_dict.get(id)
        update_qn_form.name.data = qn.get_name()
        update_qn_form.email.data = qn.get_email()
        update_qn_form.gender.data = qn.get_gender()
        update_qn_form.subject.data = qn.get_subject()
        update_qn_form.remarks.data = qn.get_remarks()
        update_qn_form.answers.data = qn.get_answers()

        return render_template('updateQn.html', form=update_qn_form)

@app.route('/deleteQn/<int:id>', methods=['POST'])
def delete_qn(id):
    qns_dict = {}
    db = shelve.open('storage.db', 'w')
    qns_dict = db['Questions']

    qns_dict.pop(id)

    db['Questions'] = qns_dict
    db.close()

    return redirect(url_for('retrieve_qns'))

# Here's the create answer app route
# @app.route("/createAns", methods=['GET', 'POST'])
# def create_qn():
#     create_qn_form = CreateQnForm(request.form)
#     if request.method == 'POST' and create_qn_form.validate():
#         qns_dict = {}
#         db = shelve.open('storage.db', 'c')

#         try:
#             qns_dict = db['Questions']
#         except:
#             print("Error in retrieving Users from storage.db.")

#         qn = Question.Question(create_qn_form.answers.data)

#         qns_dict[qn.get_qn_id()] = qn
#         db['Questions'] = qns_dict


#         return redirect(url_for('retrieve'))
#     return render_template('createQn.html', form=create_qn_form)





@app.route('/faqQn')
def retrieve():
    qns_dict = {}
    db = shelve.open('storage.db', 'r')
    qns_dict = db['Questions']
    db.close()

    qns_list = []
    for key in qns_dict:
        qn = qns_dict.get(key)
        qns_list.append(qn)
        
    return render_template('faq.html', count=len(qns_list),qns_list=qns_list)

if __name__ == '__main__':
    app.run(debug=True)

