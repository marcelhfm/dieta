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
        
        #Initialize connection to database
        config = loadConfig.Config('diet.json')
        db = Database(config)
        
        check_username = db.selectUser(username)
        
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
        
        
        #Fetch username from database and safe in variable user 
        user = db.selectUser(username)
        selected_password = user[0]['password']
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[0]['password'], password):
            error = 'Incorrect password.'
            
        if error is None:
            session.clear()
            session['user_id'] = user[0]['id']
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
        tmp = db.getUserViaID(str(user_id))
        g.user = tmp[0]
    
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view
        




    

