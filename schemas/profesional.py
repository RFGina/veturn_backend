from datetime import date
from pydantic import BaseModel


class ProfesionalBase(BaseModel):
    name: str
    email: str
    phone: str
    specialty: str


class ProfesionalCreate(ProfesionalBase):
    pass


class ProfesionalUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    specialty: str | None = None


class ProfesionalOut(ProfesionalBase):
    id: int
    veterinaria_id: int

    class Config:
        from_attributes = True
