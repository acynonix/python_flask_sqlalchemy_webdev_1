from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = 'enter_your_key_here'

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://newuser:password@localhost/scientia'


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone = db.Column(db.BigInteger)

    def __init__(self, name, designation, address, phone):
        self.name = name
        self.designation = designation
        self.address = address
        self.phone = phone




@app.route('/')
def home():
    return render_template('home.html', a='Scientia.com')


@app.route('/about')
def about():
    return render_template('about.html', a='Scientia.com')


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        designation = request.form['designation']
        address = request.form['address']
        phone = request.form['phone']
        usr = Users(name=name, designation=designation, address=address, phone=phone)
        db.session.add(usr)
        db.session.commit()
    return render_template('adduser.html')

@app.route('/delete')
def delete():
    if request.method == 'POST':
        name = request.form['name']
        try:
            Users.query.filter_by(name=name).first().delete()
            db.session.commit()
        except:
            return 'Not found'
    return render_template('deleteuser.html')



@app.route('/all')
def all_users():
    users = Users.query.all()
    return render_template('allusers.html', values=users)

@app.route('/searchuser', methods=['POST', 'GET'])
def search_user():
    if request.method == 'POST':
        try:
            name = request.form['name']
            designation = request.form['designation']
            phone = request.form['phone']
            user_by_name = Users.query.filter_by(name=name)
            user_by_designation = Users.query.filter_by(designation=designation)
            user_by_phone = Users.query.filter_by(phone=phone)
            if name:
                return render_template('searchresults.html', value=user_by_name)
            elif designation:
                return render_template('searchresults.html', value=user_by_designation)
            elif phone:
                return render_template('searchresults.html', value=user_by_phone)
        except:
            return 'User Not Found in database'
    return render_template('searchuser.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
