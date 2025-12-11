import json
from flask import Blueprint, request, jsonify
from app.models.Models import Student


kid_api = Blueprint('kid_api', __name__)

#GET: GET /api/kids/<int:parent_id>
@kid_api.route('/api/kids/<int:parent_id>', methods=['GET'])
def get_kids(parent_id):
    kids = Student.query.filter_by(parent_id=parent_id).all()
    kids_data = []
    for kid in kids:
        kids_data.append({
            "id": kid.id,
            "name": kid.name,
            "dob": kid.dob,
            "gender": kid.gender.value,
            "parent_id": kid.parent_id,
            "parent_phone": kid.parent_phone,
            "address": kid.address
        })
    return jsonify(kids_data), 200

