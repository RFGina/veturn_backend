from sqlalchemy.orm import Session
from models.models import Veterinarias, Profesionales
from .veterinaria import get_veterinaria
from schemas.profesional import ProfesionalCreate, ProfesionalUpdate
from fastapi import HTTPException


def create_profesional(db: Session, profesional_in: ProfesionalCreate, veterinaria_id: int):

    veterinaria = get_veterinaria(db, veterinaria_id)

    db_profesional = Profesionales(
        name=profesional_in.name,
        email=profesional_in.email,
        phone=profesional_in.phone,
        specialty=profesional_in.specialty,
        veterinaria_id=veterinaria_id
    )

    db.add(db_profesional)
    db.commit()
    db.refresh(db_profesional)
    return db_profesional


def getall_prof(db: Session, veterinaria_id: int, skip=0, limit=100):
    profesionales = db.query(Profesionales).filter(
        Profesionales.veterinaria_id == veterinaria_id).offset(skip).limit(limit).all()

    if not profesionales:
        raise HTTPException(
            status_code=404,
            detail="No hay profesionales en esta veterinaria"
        )

    return profesionales


def get_prof(db: Session, profesional_id: int):
    profesional = db.query(Profesionales).filter(
        Profesionales.id == profesional_id).first()

    if not profesional:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el profesional"
        )

    return profesional


def update_profesional(db: Session, profesional_id: int, profesional_in: ProfesionalUpdate):
    prof = get_prof(db, profesional_id)

    update_data = profesional_in.dict(
        exclude_unset=True)

    for field, value in update_data.items():
        setattr(prof, field, value)

    try:
        db.commit()
        db.refresh(prof)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar profesional"
        )

    return prof


def delete_prof(db: Session, profesional_id: int):
    profesional = get_prof(db, profesional_id)

    try:
        db.delete(profesional)
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar el profesional"
        )

    return {"message": "Profesional eliminado correctamente"}
