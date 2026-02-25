from app import app, db
from app.models import User, Dataset, Rule
from werkzeug.security import generate_password_hash

def seed():
    # Create admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password_hash=generate_password_hash('admin123'), is_approver=True, training_completed=True)
        db.session.add(admin)

    # Create test user
    if not User.query.filter_by(username='user').first():
        user = User(username='user', password_hash=generate_password_hash('user123'), is_approver=False, training_completed=True)
        db.session.add(user)

    # Create datasets
    if not Dataset.query.filter_by(name='Test Dataset 1').first():
        ds1 = Dataset(name='Test Dataset 1', sensitivity='Non-sensitive')
        db.session.add(ds1)
    if not Dataset.query.filter_by(name='Sensitive Dataset').first():
        ds2 = Dataset(name='Sensitive Dataset', sensitivity='Sensitive')
        db.session.add(ds2)

    db.session.commit()

    # Create rules
    ds1 = Dataset.query.filter_by(name='Test Dataset 1').first()
    if ds1 and not Rule.query.filter_by(dataset_id=ds1.id).first():
        rule = Rule(dataset_id=ds1.id, auto_approve=True)
        db.session.add(rule)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed()
    print('Database seeded.')