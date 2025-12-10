
from flask import blueprints, request, jsonify

from app.controllers.page_routes import roles_required
from app.services.student_service import search_students

student_api = blueprints.Blueprint('student_api', __name__)

#GET : GET api/students
@student_api.route('/api/students', methods=['GET'])
@roles_required('Teacher')
def get_students():
    """API endpoint để lấy danh sách học sinh dưới dạng JSON"""
    q = request.args.get('q', '', type=str).strip()
    class_id = request.args.get('class_id', type=int)
    students = search_students(q=q, class_id=class_id)

    students_data = []
    for student in students:
        students_data.append({
            'id': student.id,
            'name': student.name,
            'formatted_dob': student.formatted_dob,
            'gender': {
                'value': student.gender.value
            },
            'classroom': {
                'name': student.classroom.name
            } if student.classroom else None,
            'parent': {
                'name': student.parent.name,
                'phone': '0123456789'  # Có thể lấy từ parent.phone nếu có
            } if student.parent else None
        })

    return jsonify(students_data), 200
