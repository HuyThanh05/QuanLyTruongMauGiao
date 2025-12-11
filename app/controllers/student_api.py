from datetime import datetime
from flask import blueprints, request, jsonify
from app.utils import _get_payload
from app import db
from app.controllers.page_routes import roles_required
from app.models.Models import Student
from app.services.student_service import search_students

student_api = blueprints.Blueprint('student_api', __name__)

#GET : GET api/students
@student_api.route('/api/students', methods=['GET'])
# @roles_required('Teacher')
def get_students():

    q = request.args.get('q', '', type=str).strip()
    class_id = request.args.get('class_id', type=int)
    students = search_students(q=q, class_id=class_id)

    students_data = []
    for student in students:
        students_data.append({
            'id': student.id,
            'name': student.name,
            'dob': student.dob,
            'gender': student.gender.value,
            'class_id': student.class_id,
            'parent_id': student.parent_id,
        })

    return jsonify(students_data), 200

#PUT: api/students/<int:student_id>
@student_api.route('/api/students/<int:student_id>', methods=['PUT'])
# @roles_required('Teacher')
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "student not found"}), 404

    payload = _get_payload()
    required_fields = ['name', 'dob', 'gender', 'class_id', 'parent_id']
    for f in required_fields:
        if f not in payload:
            return jsonify({"message": f"{f} is required"}), 400

    dob_value = datetime.strptime(payload["dob"], "%d/%m/%Y").date()

    student.name = payload['name']
    student.dob = dob_value
    student.gender = payload['gender']
    student.class_id = payload['class_id']
    student.parent_id=payload['parent_id']

    db.session.commit()
    return jsonify({
        "message": "student updated",
        "student":{
            "id": student.id,
            "name": student.name,
            "dob": student.formatted_dob,
            "gender": student.gender.value,
            "class_id": student.class_id,
            "parent_id": student.parent_id
        }
    }),200

#PATCH: PATCH api/students/<int:student_id>
# @student_api.route('/api/students/<int:student_id>', methods=['PATCH'])
# @roles_required('Teacher')
# def update_student(student_id):
#     student = Student.query.get(student_id)
#     if not student:
#         return jsonify({"message": "student not found"}), 404
#
#     payload = _get_payload()
#
#     if "name" in payload:
#         student.name = payload['name']
#     if "dob" in payload:
#         student.dob = payload['dob']
#     if "gender" in payload:
#         student.gender = payload['gender']
#     if "class_id" in payload:
#         student.class_id = payload['class_id']
#     if "parent_id" in payload:
#         student.parent_id = payload['parent_id']
#     pass

