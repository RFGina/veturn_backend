from pydantic import BaseModel, EmailStr
from pydantic import BaseModel


class VeterinariaBase(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    address: str | None = None


class VeterinariaCreate(VeterinariaBase):
    password: str


class VeterinariaUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None


class VeterinariaOut(VeterinariaBase):
    id: int

    class Config:
        from_attributes = True
