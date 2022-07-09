from flask import Flask, redirect, url_for, render_template, request, session, flash

app = Flask(__name__)


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

        # return redirect(url_for('accountDetails'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    #return redirect(url_for('accountDetails'))
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

@app.route('/createEvent')
def createEvent():
    return render_template('createEvent.html')

@app.route('/myevent')
def myEvent():
    return render_template('myevent.html')   

if __name__ == '__main__':
    app.run(debug=True)
