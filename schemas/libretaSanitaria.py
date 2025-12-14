from datetime import date
from pydantic import BaseModel


class LibretaBase(BaseModel):
    vacuna: str
    fecha_vacunacion: date
    fecha_proxima_dosis: date | None = None
    observaciones: str | None = None


class LibretaCreate(LibretaBase):
    mascota_id: int
    veterinaria_id: int
    profesional: int


class LibretaUpdate(BaseModel):
    vacuna: str | None = None
    fecha_vacunacion: date | None = None
    fecha_proxima_dosis: date | None = None
    observaciones: str | None = None
    profesional: int | None = None


class LibretaOut(LibretaBase):
    id: int
    mascota_id: int
    veterinaria_id: int

    class Config:
        from_attributes = True
