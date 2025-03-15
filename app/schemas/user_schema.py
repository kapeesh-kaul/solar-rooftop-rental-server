from pydantic import BaseModel, EmailStr
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
    verified: bool = False
    moderation_status: ModerationStatus = ModerationStatus.pending
    coordinates: list[float] = []
