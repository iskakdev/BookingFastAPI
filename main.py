from fastapi import FastAPI
from booking_project.api import (booking_country, booking_user, booking_city, booking_service,
                                 booking_hotel, booking_hotel_image, booking_room,
                                 booking_room_image, booking_review, booking_booking, auth)
from booking_project.admin.setup import setup_admin
import uvicorn

booking_app = FastAPI(title='Booking Project')
booking_app.include_router(booking_country.country_router)
booking_app.include_router(booking_user.user_router)
booking_app.include_router(booking_city.city_router)
booking_app.include_router(booking_service.service_router)
booking_app.include_router(booking_hotel.hotel_router)
booking_app.include_router(booking_hotel_image.hotel_image_router)
booking_app.include_router(booking_room.room_router)
booking_app.include_router(booking_room_image.room_image_router)
booking_app.include_router(booking_review.review_router)
booking_app.include_router(booking_booking.booking_router)
booking_app.include_router(auth.auth_router)
setup_admin(booking_app)

if __name__ == '__main__':
    uvicorn.run(booking_app, host='127.0.0.1', port=8000)
