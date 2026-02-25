from app.models import AccessRequest, Rule, db
from datetime import datetime, timedelta

def process_access_request(request_id):
    req = AccessRequest.query.get(request_id)
    dataset_rule = Rule.query.filter_by(dataset_id=req.dataset_id).first()
    if dataset_rule and dataset_rule.auto_approve:
        req.status = 'Approved'
        req.expires_at = datetime.utcnow() + timedelta(days=180)
        # Grant permission logic here
    else:
        req.status = 'Pending'
    db.session.commit()
