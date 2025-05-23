# -*- coding: utf-8 -*-
# from odoo import http


# class HotelApi(http.Controller):
#     @http.route('/hotel_api/hotel_api', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hotel_api/hotel_api/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hotel_api.listing', {
#             'root': '/hotel_api/hotel_api',
#             'objects': http.request.env['hotel_api.hotel_api'].search([]),
#         })

#     @http.route('/hotel_api/hotel_api/objects/<model("hotel_api.hotel_api"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hotel_api.object', {
#             'object': obj
#         })

