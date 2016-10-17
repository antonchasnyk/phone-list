from views import *
from contacts import *
from abc import abstractmethod, ABC

from flask import Flask, render_template, request, redirect, g


app = Flask(__name__)

@app.before_request
def before():
    g.m = FileCRUD('storage.pickle')


@app.route('/')
def index():
    contacts = g.m.find_all()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods={'GET', 'POST'})
def add():
    user = phone = ''
    if request.method == 'POST':
        user = request.form.get('user')
        phone = request.form.get('phone')
        if user and phone:
            g.m.create(user, phone)
            return redirect('/')
    return render_template('add.html', user=user, phone=phone)

app.run(debug=True) # run dev web server
