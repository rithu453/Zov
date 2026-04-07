from pydantic import BaseModel, validator

class UserCreate(BaseModel):
    name: str
    email: str
    role: str

    @validator("role")
    def validate_role(cls, value):
        if value not in ["viewer", "analyst", "admin"]:
            raise ValueError("Invalid role")
        return value