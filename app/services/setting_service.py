from app import db
from app.models.Models import Setting

def get_or_create_settings():
    s = Setting.query.get(1)
    if not s:
        s = Setting(id=1, tuition_base=0, meal_fee_per_day=0, max_students_per_class=30)
        db.session.add(s)
        db.session.commit()
    return s

def update_settings(tuition_base, meal_fee_per_day, max_students_per_class, updated_by=None):
    s = get_or_create_settings()
    s.tuition_base = int(tuition_base)
    s.meal_fee_per_day = int(meal_fee_per_day)
    s.max_students_per_class = int(max_students_per_class)
    s.updated_by = updated_by
    db.session.commit()
    return s
