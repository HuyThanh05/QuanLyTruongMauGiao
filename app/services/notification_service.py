from app import db
from app.models.Models import Notification

def create_notification(title, content, target_role="All", created_by=None):
    n = Notification(
        title=title,
        content=content,
        target_role=target_role,
        created_by=created_by
    )
    db.session.add(n)
    db.session.commit()
    return n

def get_notifications_for_role(role_name: str):
    # role_name: "Parent", "Teacher"
    return (Notification.query
            .filter((Notification.target_role == "All") | (Notification.target_role == role_name))
            .order_by(Notification.created_at.desc())
            .all())
