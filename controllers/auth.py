import logging
from odoo.http import request

_logger = logging.getLogger(__name__)

def extract_token(auth_header):
    try:
        if not auth_header:
            _logger.info("No Authorization header provided.")
            return None
        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1]
            _logger.info("Token extracted: %s", token[:5] + "..." if token else "None")
            return token
        _logger.warning("Invalid Authorization header format.")
        return None
    except Exception as e:
        _logger.exception("Error extracting token: %s", e)
        return None

def authenticate_api_key(token):
    try:
        User = request.env['res.users'].sudo()
        user = user = User.search([('rest_api_key', '=', token)], limit=1)

        if user:
            _logger.info("Authenticated user: %s (ID: %s)", user.login, user.id)
        else:
            _logger.warning("No user found for token: %s", token[:5] + "..." if token else "None")
        return user
    except Exception as e:
        _logger.exception("Error during authentication: %s", e)
        return None