from flask import Flask, redirect, url_for, render_template, request, session, flash
from forms import signupForm, loginForm

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



@app.route('/accountDetails')
def accountDetails():
    return render_template('users/accountDetails.html')

@app.route('/EditAcc')
def EditAcc():
    return render_template('EditAcc.html')

@app.route('/ChangePass')
def ChangePass():
    return render_template('users/ChangePass.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



@app.route('/createEvent', methods = ['GET', 'POST'])
def createEvent():
    return render_template('createEvent.html')

@app.route('/myevent')
def myEvent():
    return render_template('myevent.html')   

if __name__ == '__main__':
    app.run(debug=True)
