import logging
from odoo.http import request

_logger = logging.getLogger(__name__)

def check_api_key():
    auth_header = request.httprequest.headers.get("Authorization")
    _logger.info("Authorization header: %s", auth_header)

    if not auth_header:
        _logger.info("No Authorization header found.")
        return None
    
    if not auth_header.startswith("Bearer "):
        _logger.info("Authorization header does not start with 'Bearer '")
        return None

    token = auth_header[7:]
    _logger.info("Extracted token: %s", token)

    # Vérification de la présence du champ api_key
    try:
        has_field = 'api_key' in request.env['res.users']._fields
        _logger.info("Model res.users has api_key field: %s", has_field)
    except Exception as e:
        _logger.error("Error checking for api_key field: %s", e)
    
    # Vérifie si le token correspond bien
    try:
        # Pour debug, compter combien d'utilisateurs ont ce token
        count = request.env['res.users'].sudo().search_count([('api_key', '=', token)])
        _logger.info("Found %d users with matching token", count)
        
        # Recherche de l'utilisateur
        user = request.env['res.users'].sudo().search([('api_key', '=', token)], limit=1)
        if user:
            _logger.info("User found: %s (ID: %s)", user.name, user.id)
            return user
        else:
            _logger.info("No user found with this token")
    except Exception as e:
        _logger.error("Error during user search: %s", e)
    
    # Vérification directe pour le user ID 8 (debug seulement)
    try:
        user_8 = request.env['res.users'].sudo().browse(8)
        if user_8.exists():
            _logger.info("User 8 exists with name: %s", user_8.name)
            _logger.info("User 8 api_key: %s", user_8.api_key)
            if user_8.api_key == token:
                _logger.info("Token matches for user 8!")
                return user_8
            else:
                _logger.info("Token does not match for user 8")
        else:
            _logger.info("User 8 does not exist")
    except Exception as e:
        _logger.error("Error checking user 8: %s", e)
    
    _logger.info("No user found with token.")
    return None