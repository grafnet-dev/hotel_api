from odoo import http
from odoo.http import request
import logging
from .auth import extract_token, authenticate_api_key
from .responses import success_response, error_response

_logger = logging.getLogger(__name__)

class UserAPIController(http.Controller):

    @http.route('/api/users', type='http', auth='none', methods=['GET'], csrf=False)
    def get_users(self, **kwargs):
        try:
            auth_header = request.httprequest.headers.get('Authorization')
            token = extract_token(auth_header)

            if not token:
                _logger.warning("Missing or invalid Authorization header.")
                return error_response("Missing or invalid Authorization header", status=401)

            api_user = authenticate_api_key(token)
            if not api_user:
                _logger.warning("Authentication failed for token.")
                return error_response("Invalid API key", status=401)

            _logger.info("API access granted to user: %s", api_user.login)

            users = request.env['res.users'].sudo().search([])
            user_data = [
                {
                    "id": user.id,
                    "name": user.name,
                    "login": user.login,
                    "email": user.email,
                }
                for user in users
            ]

            return success_response(user_data)

        except Exception as e:
            _logger.exception("Unexpected error in /api/users: %s", e)
            return error_response("Internal Server Error", status=500)
