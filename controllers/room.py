from odoo import http
from odoo.http import request
from .auth import extract_token, authenticate_api_key
from .responses import success_response, error_response
import base64
import os
base_url = os.environ.get("BASE_URL", request.httprequest.host_url.rstrip("/"))


class RoomController(http.Controller):
    
    @http.route("/api/v1/rooms", type="http", auth="none", methods=["GET"], csrf=False)
    def get_all_rooms(self, **kwargs):
        token = extract_token(request.httprequest.headers.get("Authorization"))
        user = authenticate_api_key(token)

        if not user:
            return error_response("Unauthorized", status=401)

        try:
            Room = request.env["hotel.room"].sudo()
            rooms = Room.search([])

            room_list = []
            for room in rooms:
                room_list.append(
                    {
                        "id": room.id,
                        "name": room.name,
                        "status": room.status,
                        "room_type": room.room_type,
                        "num_person": room.num_person,
                        "is_available": room.is_room_avail,
                        "is_day_use": room.is_day_use,
                        "default_check_in_time": room.default_check_in_time,
                        "default_check_out_time": room.default_check_out_time,
                        "day_use_check_in": room.day_use_check_in,
                        "day_use_check_out": room.day_use_check_out,
                        "price_per_night": room.price_per_night,
                        "day_use_price": room.day_use_price,
                        "hourly_rate": room.hourly_rate,
                        "floor": room.floor_id.name if room.floor_id else None,
                        "surface_area": room.surface_area,
                        "view": room.view_type,
                        "bed_type": room.bed_type,
                        "flooring_type": room.flooring_type,
                        "image": f"{base_url}/api/v1/rooms/image/{room.id}",  # ✅ URL vers l’image
                        "is_smoking_allowed": room.is_smoking_allowed,
                        "is_pets_allowed": room.is_pets_allowed,
                        "in_maintenance": room.is_in_maintenance,
                        "room_images": [
                        {
                            "image": f"{base_url}/api/v1/rooms/image/gallery/{img.id}"
                        } for img in room.room_image_ids
                    ],
                    }
                )

            return success_response(room_list)

        except Exception as e:
            return error_response(f"Error retrieving rooms: {str(e)}", status=500)


    @http.route("/api/v1/rooms/image/<int:room_id>", type="http", auth="none", methods=["GET"], csrf=False)
    def get_room_image(self, room_id, **kwargs):
        room = request.env["hotel.room"].sudo().browse(room_id)
        if not room.exists() or not room.image:
            return request.not_found()

        image_data = base64.b64decode(room.image)
        return request.make_response(
            image_data,
            headers=[
                ('Content-Type', 'image/jpeg'),
                ('Cache-Control', 'public, max-age=86400')
            ]
        )

    @http.route("/api/v1/rooms/image/gallery/<int:image_id>", type="http", auth="none", methods=["GET"], csrf=False)
    def get_room_gallery_image(self, image_id, **kwargs):
        image = request.env["hotel.room.image"].sudo().browse(image_id)
        if not image.exists() or not image.image:
            return request.not_found()

        image_data = base64.b64decode(image.image)
        return request.make_response(
            image_data,
            headers=[
                ('Content-Type', 'image/jpeg'),
                ('Cache-Control', 'public, max-age=86400')
            ]
        )
    
    @http.route("/api/v1/rooms/available", type="http", auth="none", methods=["GET"], csrf=False)
    def get_available_rooms(self, **kwargs):
        token = extract_token(request.httprequest.headers.get("Authorization"))
        user = authenticate_api_key(token)

        if not user:
            return error_response("Unauthorized", status=401)

        try:
            Room = request.env["hotel.room"].sudo()
            # Filtrer par disponibilité
            available_rooms = Room.search([("is_room_avail", "=", True)])  # ou ("status", "=", "available")

            room_list = []
            for room in available_rooms:
                room_list.append(
                    {
                        "id": room.id,
                        "name": room.name,
                        "status": room.status,
                        "room_type": room.room_type,
                        "num_person": room.num_person,
                        "is_available": room.is_room_avail,
                        "price_per_night": room.price_per_night,
                        "day_use_price": room.day_use_price,
                        "hourly_rate": room.hourly_rate,
                        "floor": room.floor_id.name if room.floor_id else None,
                        "surface_area": room.surface_area,
                        "view": room.view_type,
                        "bed_type": room.bed_type,
                        "image": room.image,
                        "is_smoking_allowed": room.is_smoking_allowed,
                        "is_pets_allowed": room.is_pets_allowed,
                        "in_maintenance": room.is_in_maintenance,
                        "room_images": [
                            {"image": img.image} for img in room.room_image_ids
                        ],
                        
                    }
                )

            return success_response(room_list)

        except Exception as e:
            return error_response(f"Error retrieving available rooms: {str(e)}", status=500)
