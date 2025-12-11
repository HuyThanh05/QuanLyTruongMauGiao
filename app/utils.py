from datetime import datetime

from flask import request


def _get_payload():
    return request.get_json(silent=True) or request.form

def _string_to_date(string):
    return datetime.strptime(string, "%d/%m/%Y").date()

def get_filter_params():
    q = request.args.get('q', '', type=str).strip()
    class_id = request.args.get('class_id', type=int)
    return {
        'q':q,
        'class_id':class_id
    }