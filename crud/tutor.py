from sqlalchemy.orm import Session
from models.models import Tutores
from schemas.tutor import TutorCreate, TutorUpdate
from fastapi import HTTPException
from .veterinaria import get_veterinaria


def create_tutor(db: Session, tutor_in: TutorCreate, veterinaria_id: int):
    veterinaria = get_veterinaria(db, veterinaria_id)

    db_tutor = Tutores(
        name=tutor_in.name,
        email=tutor_in.email,
        veterinaria_id=veterinaria_id
    )

    db.add(db_tutor)
    db.commit()
    db.refresh(db_tutor)

    return db_tutor


def get_tutor(db: Session, tutor_id: int):
    db_tutor = db.query(Tutores).filter(Tutores.id == tutor_id).first()

    if not db_tutor:
        raise HTTPException(
            status_code=404,
            detail="Tutor no encontrado"
        )
    return db_tutor


def get_tutor_by_email(db: Session, email: str):
    return db.query(Tutores).filter(Tutores.email == email).first()


def get_tutores(db: Session, veterinaria_id: int, skip=0, limit=100):
    return db.query(Tutores).filter(Tutores.veterinaria_id == veterinaria_id).offset(skip).limit(limit).all()


def update_tutor(db: Session, tutor_id: int, tutor_in: TutorUpdate):
    tutor_exis = get_tutor(db, tutor_id)

    update_data = tutor_in.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(tutor_exis, field, value)

    try:
        db.commit()
        db.refresh(tutor_exis)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error en actualizar el tutor"
        )


def delete_tutor(db: Session, tutor_id: int):
    tutor = get_tutor(db, tutor_id)
    if tutor:
        db.delete(tutor)
        db.commit()
    return tutor
