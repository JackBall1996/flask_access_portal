from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager
from app.models import User, Dataset, AccessRequest, Rule, AuditLog
from app.audit import log_action
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
            log_action('login', f"User '{user.username}' logged in")
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    log_action('logout', f"User '{current_user.username}' logged out")
    logout_user()
    return redirect(url_for('login'))

@app.route('/request_access', methods=['GET', 'POST'])
@login_required
def request_access():
    datasets = Dataset.query.all()
    if request.method == 'POST':
        dataset_id = request.form['dataset_id']
        purpose = request.form['purpose']
        training_confirmed = request.form.get('training_confirmed') == 'on'
        dataset = Dataset.query.get(dataset_id)
        if not training_confirmed:
            flash('You must confirm training completion.')
            return render_template('request_access.html', datasets=datasets)
        req = AccessRequest(
            user_id=current_user.id,
            dataset_id=dataset_id,
            access_type=dataset.sensitivity,  # Inherit sensitivity from dataset
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
    requests = (
        AccessRequest.query
        .filter_by(user_id=current_user.id)
        .join(Dataset, AccessRequest.dataset_id == Dataset.id)
        .add_entity(Dataset)
        .all()
    )
    # requests is now a list of tuples: (AccessRequest, Dataset)
    return render_template('my_requests.html', requests=requests)


# Approver dashboard: view and act on pending requests
@app.route('/approver/dashboard', methods=['GET', 'POST'])
@login_required
def approver_dashboard():
    if not current_user.is_approver:
        flash('Approver access required.')
        return redirect(url_for('index'))
    # Handle approve/reject actions
    if request.method == 'POST':
        req_id = request.form.get('request_id')
        action = request.form.get('action')
        reason = request.form.get('reason', '')
        access_request = AccessRequest.query.get(req_id)
        if access_request and access_request.status == 'Pending':
            if action == 'approve':
                access_request.status = 'Approved'
                access_request.approver_id = current_user.id
                access_request.decision_reason = reason
                access_request.expires_at = datetime.utcnow() + timedelta(days=180)
                # Grant permission logic here
                flash(f'Request {req_id} approved.')
            elif action == 'reject':
                access_request.status = 'Rejected'
                access_request.approver_id = current_user.id
                access_request.decision_reason = reason
                flash(f'Request {req_id} rejected.')
            db.session.commit()
    # Use aliases to avoid join ambiguity
    from sqlalchemy.orm import aliased
    Requester = aliased(User)
    pending_requests = (
        AccessRequest.query
        .join(Dataset, AccessRequest.dataset_id == Dataset.id)
        .join(Requester, AccessRequest.user_id == Requester.id)
        .add_entity(Dataset)
        .add_entity(Requester)
        .filter(AccessRequest.status == 'Pending', Dataset.sensitivity == 'Sensitive')
        .all()
    )
    # pending_requests is a list of tuples: (AccessRequest, Dataset, Requester)
    return render_template('approver_dashboard.html', requests=pending_requests)
