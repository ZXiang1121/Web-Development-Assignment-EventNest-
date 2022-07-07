from flask import Flask, redirect, url_for, render_template, request, session, flash

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/ticketdetails')
def ticketdetails():
    return render_template('ticketdetails.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
