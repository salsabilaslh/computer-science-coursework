from pydantic import BaseModel, field_validator

class UserCreate(BaseModel):
    """Schema for validating data when creating a new user."""
    name: str
    email: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty or just whitespace.")
        return v

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v: str) -> str:
        v = v.strip()
        if "@" not in v:
            raise ValueError("Invalid email address. It must contain '@'.")
        return v

class UserResponse(BaseModel):
    """Schema for structured API response sent back to the client."""
    id: int
    name: str
    email: str