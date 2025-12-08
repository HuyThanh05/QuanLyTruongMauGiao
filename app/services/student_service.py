from typing import List

from app.models.Models import Student, Classroom


def get_all_students() -> List[Student]:
    return Student.query.all()

def total_student(classrooms: List[Classroom])->int:
    return sum(classroom.max_slots for classroom in classrooms)

def search_students(q=None) -> List[Student]:
    student_query = Student.query

    if q:
        q=q.strip()
        like_pattern = f"%{q}%"
        student_query = student_query.filter(Student.name.ilike(like_pattern))

    return student_query.all()