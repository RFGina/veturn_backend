from datetime import date
from pydantic import BaseModel


class EspecieBase(BaseModel):
    nombre: str
    description: str | None = None


class EspecieCreate(EspecieBase):
    pass


class EspecieUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class EspecieOut(EspecieBase):
    id: int

    class Config:
        from_attributes = True


class MascotaBase(BaseModel):
    name: str
    description: str | None = None
    birth_date: date
    especie_id: int


class MascotaCreate(MascotaBase):
    pass


class MascotaUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    birth_date: date | None = None
    tutor_id: int | None = None
    especie_id: int | None = None


class MascotaOut(MascotaBase):
    id: int
    tutor_id: int
    veterinaria_id: int
    especie_id: int

    class Config:
        from_attributes = True
