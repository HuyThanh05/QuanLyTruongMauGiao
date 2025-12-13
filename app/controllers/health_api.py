from flask import Blueprint, jsonify

from app import db
from app.models.Models import HealthRecord, Student
from app.utils import format_date, time_ago, _get_payload

health_api = Blueprint('health_api', __name__)

#GET: GET /api/health
@health_api.route('/api/health', methods=['GET'])
def get_all_health_record():
    health_records = HealthRecord.query.all()
    if not health_records:
        return jsonify({
            "messgage": "no health record"
        })
    health_records_data = []
    for record in health_records:
        health_records_data.append({
            "id": record.id,
            "student":{
                "id": record.student.id,
                "name": record.student.name,
            },
            "teacher":{
                "id": record.teacher.id,
                "name": record.teacher.name,
            },
            "height": record.height,
            "weight": record.weight,
            "temperature" : record.temperature,
            "note" : record.note,
            "date": format_date(record.date_created)
        })

    return jsonify(health_records_data),200

#GET: GET /api/health/<int:student_id>
@health_api.route('/api/health/<int:student_id>', methods=['GET'])
def get_health_record_by_student_id(student_id):
    health_records = HealthRecord.query.filter_by(student_id=student_id).order_by(HealthRecord.date_created.asc()).all()
    if not health_records:
        return jsonify({
            "messgage": "no health record"
        })

    health_records_data = []
    for record in health_records:
        health_records_data.append({
            "id": record.id,
            "student":{
                "id": record.student.id,
                "name": record.student.name,
            },
            "height": record.height,
            "weight": record.weight,
            "temperature" : record.temperature,
            "note" : record.note,
            "date_created": format_date(record.date_created),
            "time_ago": time_ago(record.date_created),
            "teacher":{
                "id": record.teacher.id if record.teacher else None,
                "name": record.teacher.name if record.teacher else None,
            }
        })
    return jsonify(health_records_data),200



#POST: POST /api/health/<int:student_id>/health-records/<int:record_id>
@health_api.route('/api/health/<int:student_id>/health-records', methods=['POST'])
def create_health_record_by_id(student_id):
    payload = _get_payload()
    health_record = HealthRecord(
        student_id=student_id,
        weight=payload['weight'],
        height=payload['height'],
        temperature=payload['temperature'],
        note=payload['note']
    )
    db.session.add(health_record)
    db.session.commit()
    return jsonify({
        "message": "created successfully",
        "data":{
            "id": health_record.id,
            "student_id": student_id,
            "weight": payload['weight'],
            "height": payload['height'],
            "temperature": payload['temperature'],
            "note": payload['note'],
            "time_ago": time_ago(health_record.date_created)
        }
    }),201

#PUT: PUT /api/health/<int:student_id>/health-records/<int:record_id>
@health_api.route('/api/health/<int:student_id>/health-records/<int:record_id>', methods=['PUT'])
def update_health_record_by_id(student_id, record_id):
    payload = _get_payload()
    health_record = HealthRecord.query.filter_by(student_id=student_id, id=record_id).first()
    if not health_record:
        return jsonify({"messgage": "not found"}),404
    health_record.weight = payload['weight']
    health_record.height = payload['height']
    health_record.temperature = payload['temperature']
    health_record.note = payload['note']
    db.session.commit()
    return jsonify({
        "message": "updated successfully",
        "data":{
            "id": health_record.id,
            "student_id": student_id,
            "weight": payload['weight'],
            "height": payload['height'],
            "temperature": payload['temperature'],
            "note": payload['note']
        }
    })