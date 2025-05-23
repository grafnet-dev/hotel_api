from odoo import api, fields, models
import secrets

class ResUsers(models.Model):
    _inherit = 'res.users'

    rest_api_key = fields.Char(string='REST API Key', copy=False)

    def generate_rest_api_key(self):
            for user in self:
                user.rest_api_key = secrets.token_hex(32)
            #self.write({})  # Force la sauvegarde en DB 
