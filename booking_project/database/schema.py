from pydantic import BaseModel, EmailStr
from typing import Optional
from .models import RoleChoices, RoomTypeChoices, RoomStatusChoices
from datetime import date, datetime


class CountryInputSchema(BaseModel):
    country_image: str
    country_name: str


class CountryOutSchema(BaseModel):
    id: int
    country_image: str
    country_name: str


class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    age: Optional[int]
    phone_number: Optional[str]
    country_id: int


class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    age: Optional[int]
    phone_number: Optional[str]
    status: RoleChoices
    registered_date: datetime
    country_id: int


class UserLoginSchema(BaseModel):
    username: str
    password: str


class CityInputSchema(BaseModel):
    city_image: str
    city_name: str
    country_id: int


class CityOutSchema(BaseModel):
    id: int
    city_image: str
    city_name: str
    country_id: int


class ServiceInputSchema(BaseModel):
    service_image: str
    service_name: str


class ServiceOutSchema(BaseModel):
    id: int
    service_image: str
    service_name: str


class HotelInputSchema(BaseModel):
    street: str
    postal_code: int
    hotel_stars: int
    description: str
    country_id: int
    city_id: int
    service_id: int
    owner_id: Optional[int]


class HotelOutSchema(BaseModel):
    id: int
    street: str
    postal_code: int
    hotel_stars: int
    description: str
    country_id: int
    city_id: int
    service_id: int
    owner_id: Optional[int]


class HotelImageInputSchema(BaseModel):
    hotel_image: str
    hotel_id: int


class HotelImageOutSchema(BaseModel):
    id: int
    hotel_image: str
    hotel_id: int


class RoomInputSchema(BaseModel):
    room_number: int
    price: int
    room_type: RoomTypeChoices
    room_status: RoomStatusChoices
    description: str
    hotel_id: int


class RoomOutSchema(BaseModel):
    id: int
    room_number: int
    price: int
    room_type: RoomTypeChoices
    room_status: RoomStatusChoices
    description: str
    hotel_id: int


class RoomImageInputSchema(BaseModel):
    room_image: str
    hotel_id: int


class RoomImageOutSchema(BaseModel):
    id: int
    room_image: str
    hotel_id: int


class ReviewInputSchema(BaseModel):
    rating: int
    comment: str
    user_id: int
    hotel_id: int


class ReviewOutSchema(BaseModel):
    id: int
    rating: int
    comment: str
    created_add: datetime
    user_id: int
    hotel_id: int


class BookingInputSchema(BaseModel):
    check_in: date
    check_out: date
    user_id: int
    hotel_id: int
    room_id: int


class BookingOutSchema(BaseModel):
    id: int
    check_in: date
    check_out: date
    created_date: datetime
    user_id: int
    hotel_id: int
    room_id: int
