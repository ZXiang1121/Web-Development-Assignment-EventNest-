from flask import Flask, redirect, url_for, render_template, request, session, flash
import shelve, account

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

        # return redirect(url_for('accountDetails'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('signup.html')



@app.route('/accountDetails')
def accountDetails():
    return render_template('accountDetails.html')

@app.route('/EditAcc')
def EditAcc():
    return render_template('EditAcc.html')

@app.route('/ChangePass')
def ChangePass():
    return render_template('ChangePass.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



@app.route('/createEvent', methods = ['GET', 'POST'])
def createEvent():
    # create_event_form = CreateEventForm(request.form)

    # if request.method == 'POST' and create_event_form.validate():
    #     events_dict = {}
    #     db = shelve.open('storage.db', 'c')

    #     try:
    #         events_dict = db['Events']
    #     except:
    #         print("Error in retrieving Users from storage.db.")
        
    #     event = Event.Event(create_event_form.event_name.data,
    #                         create_event_form.num_ticket.data,
    #                         create_event_form.event_price.data,
    #                         create_event_form.seat_type.data,
    #                         create_event_form.event_date.data,
    #                         # create_event_form.event_image.data,
    #                         create_event_form.description.data
    #                         )
    #     events_dict[event.get_event_name()] = event
    #     db['Events'] = events_dict
        
    #     #Test Code
    #     events_dict = db['Events']
    #     event = events_dict[event.get_event_name()]
    #     print(event.get_event_location(), event.get_event_date(), "was stored in storage.db successfully with event_name ==", event.get_event_name)

    #     db.close()


    #     return redirect(url_for('home'))
    return render_template('createEvent.html', form=create_event_form)

@app.route('/myevent')
def myEvent():
    return render_template('myevent.html')   

if __name__ == '__main__':
    app.run(debug=True)
