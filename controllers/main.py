from odoo import http
from odoo.http import request
from .utils import check_api_key  # adapte selon ton projet
import logging

_logger = logging.getLogger(__name__)

class MyApiController(http.Controller):

    @http.route('/myapi/secure-data', type='json', auth='none', methods=['POST'], csrf=False)
    def secure_data(self, **kwargs):
        _logger.info("==== /myapi/secure-data called ====")

        user = check_api_key()
        if not user:
            _logger.warning("Authentication failed: Invalid or missing token.")
            return {"error": "Unauthorized"}

        _logger.info("Authenticated user: %s (ID: %s)", user.name, user.id)
        return {"message": f"Hello {user.name}, access granted!"}
