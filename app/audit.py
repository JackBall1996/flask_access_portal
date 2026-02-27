from app import db
from app.models import AuditLog
from flask_login import current_user
from datetime import datetime

def log_action(action, details):
    log = AuditLog(
        user_id=current_user.id,
        username=current_user.username,
        action=action,
        details=details,
        timestamp=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()
