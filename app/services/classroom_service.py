from app import db
from app.models.Models import Classroom, User, Role

def get_teachers():
    # User.roles là many-to-many -> join Role để lọc Teacher
    return User.query.join(User.roles).filter(Role.name == "Teacher").all()

def assign_teacher_to_class(class_id: int, teacher_id: int | None):
    classroom = Classroom.query.get(class_id)
    if not classroom:
        return None, "Không tìm thấy lớp"

    if not teacher_id:
        classroom.teacher_id = None
        db.session.commit()
        return classroom, None

    teacher = User.query.get(teacher_id)
    if not teacher:
        return None, "Không tìm thấy giáo viên"

    # Check role Teacher
    if not any(r.name == "Teacher" for r in teacher.roles):
        return None, "User này không có role Teacher"

    classroom.teacher_id = teacher_id
    db.session.commit()
    return classroom, None
