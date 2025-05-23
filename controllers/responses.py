from odoo.http import request

def success_response(data):
    return request.make_json_response({"success": True, "data": data}, status=200)

def error_response(message, status=400):
    return request.make_json_response({"success": False, "error": message}, status=status)
