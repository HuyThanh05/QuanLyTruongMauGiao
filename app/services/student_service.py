from typing import List

from app.models.DTO import StudentDTO
from app.models.Models import Student, Classroom


def get_all_students() -> List[Student]:
    return Student.query.all()

def get_student_by_classroom(classroom: Classroom) -> List[Student]:
    return Student.query.filter_by(classroom = classroom.id).all()

def get_student_count_by_classroom(classroom_id: int) -> int:
    return Student.query.filter_by(class_id=classroom_id).count()

def total_student(classrooms: List[Classroom]) -> int:
    if not classrooms:
        return 0
    classroom_ids = [classroom.id for classroom in classrooms]
    return Student.query.filter(Student.class_id.in_(classroom_ids)).count()

def search_students(q=None, class_id=None) -> List[Student]:
    student_query = Student.query

    if q:
        q = q.strip()
        like_pattern = f"%{q}%"
        student_query = student_query.filter(Student.name.ilike(like_pattern))

    if class_id:
        student_query = student_query.filter_by(class_id=class_id)

    return student_query.all()

# def student_to_dto(student: Student) -> StudentDTO:
