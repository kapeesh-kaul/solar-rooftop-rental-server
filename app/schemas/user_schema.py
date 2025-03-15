from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    name: str
    email: EmailStr
    address: str
    rate: float
    verified: bool = False
    moderated: bool = False
    coordinates: list[float] = []
