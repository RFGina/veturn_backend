from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, time


class EstadoTurnoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50,
                        description="Nombre del estado")
    descripcion: Optional[str] = Field(
        None, max_length=500, description="Descripción del estado")


class EstadoTurnoCreate(EstadoTurnoBase):
    pass


class EstadoTurnoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=500)


class EstadoTurnoOut(EstadoTurnoBase):
    id: int

    class Config:
        from_attributes = True


class EstadoTurnoConTurnos(EstadoTurnoOut):
    turnos: list["TurnoOut"] = []

    class Config:
        from_attributes = True


class TurnoBase(BaseModel):
    fecha_hora: datetime = Field(..., description="Fecha y hora del turno")
    notes: Optional[str] = Field(
        None, max_length=500, description="Notas adicionales")
    estado_id: int = Field(
        default=1, description="ID del estado del turno (1=pendiente por defecto)")


class TurnoCreate(TurnoBase):
    mascota_id: int = Field(..., description="ID de la mascota")
    detalle_servicio_id: int = Field(
        ..., description="ID del detalle de servicio (servicio + profesional)")

    @validator('fecha_hora')
    def fecha_no_pasada(cls, v):
        # Si la fecha tiene timezone, convertirlo a naive (sin timezone)
        if v.tzinfo is not None:
            # Opción A: Quitar el timezone completamente
            v = v.replace(tzinfo=None)
            # Opción B: Convertir a hora local
            # v = v.astimezone().replace(tzinfo=None)

        # Ahora comparar con datetime.now() (que también es naive)
        if v < datetime.now():
            raise ValueError('El turno no puede ser en el pasado')
        return v


class TurnoUpdate(BaseModel):
    fecha_hora: Optional[datetime] = Field(
        None, description="Nueva fecha y hora")
    detalle_servicio_id: Optional[int] = Field(
        None, description="Nuevo detalle de servicio")
    estado_id: Optional[int] = Field(
        None, description="Nuevo estado del turno")
    notes: Optional[str] = Field(
        None, max_length=500, description="Notas actualizadas")

    @validator('fecha_hora')
    def fecha_no_pasada(cls, v):
        if v and v < datetime.now():
            raise ValueError('El turno no puede ser en el pasado')
        return v


class TurnoOut(TurnoBase):
    id: int
    mascota_id: int
    detalle_servicio_id: int
    veterinaria_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
