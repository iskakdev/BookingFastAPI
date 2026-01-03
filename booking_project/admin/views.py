from booking_project.database.models import (UserProfile, Country,
                                             City, Service, Hotel,
                                             HotelImage, Room, RoomImage,
                                             Review, Booking)
from sqladmin import ModelView


class CountryAdmin(ModelView, model=Country):
    column_list = [Country.id, Country.country_name]


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.first_name, UserProfile.last_name]


class CityAdmin(ModelView, model=City):
    column_list = [City.id, City.city_name]


class ServiceAdmin(ModelView, model=Service):
    column_list = [Service.service_name]


class HotelAdmin(ModelView, model=Hotel):
    column_list = [Hotel.id, Hotel.hotel_country, Hotel.hotel_city]


class HotelImageAdmin(ModelView, model=HotelImage):
    column_list = [HotelImage.id, HotelImage.hotel_image]


class RoomAdmin(ModelView, model=Room):
    column_list = [Room.id, Room.room_number, Room.room_type, Room.room_status]


class RoomImageAdmin(ModelView, model=RoomImage):
    column_list = [RoomImage.id, RoomImage.room_image]


class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.id, Review.user_review, Review.comment]


class BookingAdmin(ModelView, model=Booking):
    column_list = [Booking.id, Booking.user_id, Booking.hotel_id, Booking.room_id,
                   Booking.check_in, Booking.check_out]
