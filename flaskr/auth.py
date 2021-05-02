import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.dietDB import Database 
import loadConfig

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        check_username = None
        
        #Initialize connection to database
        config = loadConfig.Config('diet.json')
        db = Database(config)
        
        try:
            user_id = db.getUserID(username)[0]["id"]
            check_username = db.selectUser(user_id)[0]["username"]
        except:
            pass
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif username == check_username:
            error = 'User {} is alerady registered.'.format(username)
        
        if error is None:
            data = {
                "username": username,
                "password": password
            }
            db.insertUser(data)
            return redirect(url_for('auth.login'))
        
        flash(error)
        
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #Initialize connection to database
        config = loadConfig.Config('diet.json')
        db = Database(config)
        error = None
        user = None
        
        #Fetch username from database and safe in variable user 
        try:
            user_id = db.getUserID(username)[0]["id"]
            user = db.selectUser(user_id)
            selected_password = user[0]['password']
        except:
            error = "User with given username does not exist"
            
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(selected_password, password):
            error = 'Incorrect password.'
            
        if error is None:
            session.clear()
            session['user_id'] = user_id
            return redirect(url_for('configure.calculate'))
        
        flash(error)
        
    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    #Initialize connection to database
    config = loadConfig.Config('diet.json')
    db = Database(config)

    if user_id is None:
        g.user = None
    else:
        tmp = db.selectUser(user_id)
        g.user = tmp[0]
    
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view
        




    

