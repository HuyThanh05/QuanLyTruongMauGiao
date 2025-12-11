from flask import request


def _get_payload():
    return request.get_json(silent=True) or request.form