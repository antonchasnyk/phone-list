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
    con = [ {'user': contact[0], 'phone': contact[1]} for contact in contacts ]
    return render_template('index.html', contacts=con)


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


@app.route('/edit/<name>', methods={'GET', 'POST'})
def edit(name):
    phone = ''
    if request.method == 'POST':
        phone = request.form.get('phone')
        if phone:
            g.m.update(name, lambda x: phone)
            return redirect('/')
    return render_template('edit.html', phone=phone)

@app.route('/del/<name>', methods={'GET', 'POST'})
def delete(name):
    if request.method == 'POST':
        g.m.delete(name)
        return redirect('/')
    return render_template('del.html')

app.run(debug=True) # run dev web server
