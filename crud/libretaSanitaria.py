from sqlalchemy.orm import Session
from schemas.libretaSanitaria import LibretaCreate, LibretaUpdate
from .veterinaria import get_veterinaria
from .mascota import get_mascota
from .profesional import get_prof
from models.models import LibretaSanitaria, Mascotas, Profesionales
from fastapi import HTTPException


def createLibreta(db: Session, libreta_in: LibretaCreate, veterinaria_id: int):
    veterinaria = get_veterinaria(db, veterinaria_id)
    mascota = db.query(Mascotas).filter(
        Mascotas.id == libreta_in.mascota_id).first()
    profesional = db.query(Profesionales).filter(
        Profesionales.id == libreta_in.Profesionales_id).first()

    db_libreta = LibretaSanitaria(
        vacuna=libreta_in.vacuna,
        fecha_vacunacion=libreta_in.fecha_vacunacion,
        fecha_proxima_dosis=libreta_in.fecha_proxima_dosis,
        observaciones=libreta_in.observaciones,
        veterinaria_id=libreta_in.veterinaria_id,
        mascota_id=libreta_in.mascota_id,
        profesional_id=libreta_in.profesional_id
    )

    db.add(db_libreta)
    db.commit()
    db.refresh(db_libreta)
    return db_libreta


def getAll_libreta(db: Session, veterinaria_id: int):
    resultado = db.query(LibretaSanitaria).filter(
        LibretaSanitaria.veterinaria_id == veterinaria_id).all()

    if not resultado:
        raise HTTPException(
            status_code="404",
            detail="No hay libretas que mostrar"
        )
    return resultado


def get_libreta(db: Session, libreta_id: int):
    resultado = db.query(LibretaSanitaria).filter(
        LibretaSanitaria.id == libreta_id).first()

    if not resultado:
        raise HTTPException(
            status_code="404",
            detail="No se encuentra la libreta"
        )
    return resultado


def updateLibreta(db: Session, libreta_in: LibretaUpdate, libreta_id):
    libreta = get_libreta(db, libreta_id)

    update_libreta = libreta_in.dict(exclude_unset=True)

    for field, value in update_libreta.items():
        setattr(libreta, field, value)

    try:
        db.commit()
        db.refresh(libreta)
    except Exception:
        db.rollback()
        HTTPException(
            status_code="500",
            detail="No se pudo actualizar la libreta"
        )
    return libreta


def deleteLibreta(db: Session, libreta_id: int):
    libreta = get_libreta(libreta_id)

    db.delete(libreta)
    db.commit()
