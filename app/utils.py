from datetime import datetime

from flask import request


def format_date(date):
    return date.strftime("%d/%m/%Y")

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

from datetime import datetime

def time_ago(dt: datetime):
    now = datetime.utcnow()
    diff = now - dt

    seconds = diff.total_seconds()

    if seconds < 60:
        return f"{int(seconds)} giây trước"
    if seconds < 3600:
        return f"{int(seconds // 60)} phút trước"
    if seconds < 86400:
        return f"{int(seconds // 3600)} giờ trước"
    if seconds < 2592000:
        return f"{int(seconds // 86400)} ngày trước"
    if seconds < 31536000:
        return f"{int(seconds // 2592000)} tháng trước"
    return f"{int(seconds // 31536000)} năm trước"
