from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager
from app.models import User, Dataset, AccessRequest, Rule, AuditLog
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            AuditLog(user_id=user.id, action='login', details='User logged in')
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    AuditLog(user_id=current_user.id, action='logout', details='User logged out')
    logout_user()
    return redirect(url_for('login'))

@app.route('/request_access', methods=['GET', 'POST'])
@login_required
def request_access():
    datasets = Dataset.query.all()
    if request.method == 'POST':
        dataset_id = request.form['dataset_id']
        access_type = request.form['access_type']
        purpose = request.form['purpose']
        training_confirmed = request.form.get('training_confirmed') == 'on'
        dataset = Dataset.query.get(dataset_id)
        if not training_confirmed:
            flash('You must confirm training completion.')
            return render_template('request_access.html', datasets=datasets)
        req = AccessRequest(
            user_id=current_user.id,
            dataset_id=dataset_id,
            access_type=access_type,
            purpose=purpose,
            status='Pending',
            requested_at=datetime.utcnow()
        )
        db.session.add(req)
        db.session.commit()
        # Rules engine will process this request
        return redirect(url_for('my_requests'))
    return render_template('request_access.html', datasets=datasets)

@app.route('/my_requests')
@login_required
def my_requests():
    requests = AccessRequest.query.filter_by(user_id=current_user.id).all()
    return render_template('my_requests.html', requests=requests)

# ... more routes for admin, approver dashboard, etc.
