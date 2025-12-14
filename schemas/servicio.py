from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional


class ServicioBase(BaseModel):
    name: str
    description: str


class ServicioCreate(ServicioBase):
    pass


class ServicioUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ServicioOut(ServicioBase):
    id: int
    veterinaria_id: int

    class Config:
        from_attributes = True


class DetalleServicioBase(BaseModel):
    profesional_id: int
    servicio_id: int


class DetalleServicioCreate(DetalleServicioBase):
    pass


class DetalleServicioUpdate(BaseModel):
    servicio_id: int | None = None
    profesional_id: int | None = None


class DetalleServicioOut(BaseModel):
    id: int
    servicio_id: int
    nombre_servicio: Optional[str] = None
    profesional_id: int
    nombre_profesional: Optional[str] = None
    veterinaria_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
