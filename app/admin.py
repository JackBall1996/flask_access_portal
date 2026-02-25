from app import app, db
from app.models import Dataset, Rule
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

@app.route('/admin/datasets', methods=['GET', 'POST'])
@login_required
def manage_datasets():
    if not current_user.is_approver:
        flash('Admin access required.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        sensitivity = request.form['sensitivity']
        dataset = Dataset(name=name, sensitivity=sensitivity)
        db.session.add(dataset)
        db.session.commit()
        flash('Dataset added.')
    datasets = Dataset.query.all()
    return render_template('admin_datasets.html', datasets=datasets)

@app.route('/admin/rules', methods=['GET', 'POST'])
@login_required
def manage_rules():
    if not current_user.is_approver:
        flash('Admin access required.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        dataset_id = request.form['dataset_id']
        auto_approve = request.form.get('auto_approve') == 'on'
        rule = Rule(dataset_id=dataset_id, auto_approve=auto_approve)
        db.session.add(rule)
        db.session.commit()
        flash('Rule added.')
    rules = Rule.query.all()
    datasets = Dataset.query.all()
    return render_template('admin_rules.html', rules=rules, datasets=datasets)
