from flask import jsonify

def api_error(msg):
    return jsonify(error=msg)