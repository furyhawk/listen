from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseResponse):
    token_type: str = "Bearer"
    access_token: str
    expires_at: int
    refresh_token: str
    refresh_token_expires_at: int


class UserResponse(BaseResponse):
    user_id: str
    email: EmailStr


class PetResponse(BaseResponse):
    id: int
    pet_name: str
    user_id: str


class TemperatureResponse(BaseResponse):
    id: int
    temperature: str
    update_time: datetime


class HumidityResponse(BaseResponse):
    id: int
    humidity: str
    update_time: datetime


class PressureResponse(BaseResponse):
    id: int
    pressure: str
    update_time: datetime
