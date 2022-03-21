
from cgi import print_exception
from crypt import methods
from unicodedata import category
from market import app
from flask import render_template,redirect,url_for,flash,get_flashed_messages, request
from market import forms
from market.models import Item,User
from market.forms import Register,Login,Buy,Sell
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/market', methods=['GET','POST'])
@login_required
def market():
    buy_form = Buy()
    sell_form= Sell()
    if request.method == 'POST':
        #for purchase
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(item_name = purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash('Purchase successfull!', category='success')
            else:
                flash('Budget requirement not met!', category='danger')

        #for selling
        sold_item =request.form.get('sold_item')
        s_item_object =Item.query.filter_by(item_name = sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash('Sold successfully!', category ='success')
            else:
                flash('Item not sellable', category='danger')
            


        return redirect(url_for('market'))


    
    if request.method == 'GET':
            items= Item.query.filter_by(owner = None)
            owned_items = Item.query.filter_by(owner = current_user.id)
            return render_template('market.html', items=items, buy_form=buy_form, owned_items=owned_items, sell_form=sell_form)

@app.route('/register',methods=['GET' , 'POST'])
def registerpage():
    form = Register()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
                            emailadd=form.emailaddress.data,
                            password1 = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)

        flash(f'Registered Successfully! You are now logged in as {user_to_create.username}',category='success')
        return redirect(url_for('market'))
    
    if form.errors !={}:
        for err in form.errors.values():
            flash(f'Error: {err}',category='danger')


    return render_template('register2.html', form =form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            login_user(attempted_user)
            flash(f'You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('market'))
        else:
            flash(f'Invalid Username and Password', category='danger')


    return render_template('login.html',form =form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('index'))