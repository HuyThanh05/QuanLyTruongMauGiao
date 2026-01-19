from datetime import date
from sqlalchemy import func
from app import db
from app.models.Models import HealthRecord, Student

def count_students_recorded_today():
    today = date.today()

    count= (
        db.session.query(func.count(func.distinct(HealthRecord.student_id)))
        .filter(func.date(HealthRecord.date_created) == today)
        .scalar()
    )
    return count

def count_students_not_recorded_today():
    today = date.today()

    recorded_today = count_students_recorded_today()
    all_students = db.session.query(func.count(Student.id)).scalar()
    not_recorded_today = all_students - recorded_today
    return not_recorded_today

def count_student_record(student_id):
    health_record = HealthRecord.query.filter_by(student_id=student_id).count()
    return health_record