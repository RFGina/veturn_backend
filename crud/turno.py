from sqlalchemy.orm import Session
from database.db import get_db
from schemas.turno import TurnoCreate, EstadoTurnoCreate, TurnoUpdate
from models.models import Turnos, EstadoTurno, Veterinarias, Mascotas, DetalleServicio, Mascotas
from .veterinaria import get_veterinaria
from .mascota import get_mascota
from .servicio import get_detalle_servicio_veterinaria
from fastapi import HTTPException, Depends


def crearEstadoTurno(db: Session, estado_in: EstadoTurnoCreate):
    db_estadoT = EstadoTurno(
        nombre=estado_in.nombre,
        descripcion=estado_in.descripcion
    )
    db.add(db_estadoT)
    db.commit()
    db.refresh(db_estadoT)
    return db_estadoT


def get_estados(db: Session, skip=0, limit=100):

    resultado = db.query(EstadoTurno).offset(skip).limit(limit).all()

    return resultado


def get_estado(db: Session, estado_id: int):
    resultado = db.query(EstadoTurno).filter(
        EstadoTurno.estado_id == estado_id).first()

    if not resultado:
        raise HTTPException(
            status_code="404",
            detail="No se encontraron detalles, revisa nuevamente"
        )
    return resultado


def crearTurno(db: Session, turno_in: TurnoCreate, veterinaria_id: int):

    estado = db.query(EstadoTurno).filter(
        EstadoTurno.id == turno_in.estado_id).first()
    if not estado:
        raise HTTPException(
            status_code=404, detail="EstadoTurno no encontrado")

    mascota = db.query(Mascotas).filter(
        Mascotas.id == turno_in.mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    detalle_servicio = db.query(DetalleServicio).filter(
        DetalleServicio.id == turno_in.detalle_servicio_id).first()
    if not detalle_servicio:
        raise HTTPException(
            status_code=404, detail="DetalleServicio no encontrado")

    # Crear el turno usando las COLUMNAS de ID, no las relaciones
    db_turno = Turnos(
        fecha_hora=turno_in.fecha_hora,
        notes=turno_in.notes,
        # Usar las columnas _id, no las relaciones
        estado_id=turno_in.estado_id,
        mascota_id=turno_in.mascota_id,
        detalle_servicio_id=turno_in.detalle_servicio_id,
        veterinaria_id=veterinaria_id
    )

    db.add(db_turno)
    db.commit()
    db.refresh(db_turno)
    return db_turno


def getAllTurnos(db: Session, veterinaria_id: int):
    turnos = db.query(Turnos).filter(
        Turnos.veterinaria_id == veterinaria_id).all()
    if not turnos:
        raise HTTPException(
            status_code="404",
            detail="No hay turnos disponibles en este momento"
        )
    return turnos


def getTurno(db: Session, turno_id: int):
    turno = db.query(Turnos).filter(Turnos.id == turno_id).first()

    if not turno:
        raise HTTPException(
            status_code="404",
            detail="No se encuentra el turno seleccionado"
        )
    return turno


def updateTurno(db: Session, turno_in: TurnoUpdate, turno_id: int):
    turno = getTurno(db, turno_id)

    editar_datos = turno_in.dict(exclude_unset=True)

    for field, value in editar_datos.items():
        setattr(turno, field, value)

    try:
        db.commit()
        db.refresh(turno)
    except Exception:
        HTTPException(
            status_code="500",
            detail="No se pudo actualizar el turno"
        )
    return turno


def deleteTurno(db: Session, turno_id: int):
    turno = getTurno(db, turno_id)

    try:
        db.delete(turno)
        db.commit()
        db.refresh(turno)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar el turno"
        )

    return turno
