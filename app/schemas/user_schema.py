from pydantic import BaseModel, EmailStr, AnyUrl 
from enum import Enum

class ModerationStatus(str, Enum):
        pending = "pending"
        accepted = "accepted"
        rejected = "rejected"

class UserSchema(BaseModel):
    name: str
    email: EmailStr
    address: str
    rate: float
    bill_url: str
    satellite_image_url : str = 'not.here'
    area_square_feet : float = 0
    verified: bool = False
    moderation_status: ModerationStatus = ModerationStatus.pending
    coordinates: list[float] = []
