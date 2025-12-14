from sqlalchemy.orm import Session
from models.models import Mascotas, Veterinarias, Especies, Tutores
from schemas.mascota import MascotaCreate, MascotaUpdate, EspecieCreate
from passlib.context import CryptContext
from fastapi import HTTPException
from .tutor import get_tutor
from .veterinaria import get_veterinaria


def create_especies(db: Session, especie_in: EspecieCreate):
    db_especie = Especies(
        nombre=especie_in.nombre,
        descripcion=especie_in.description,

    )

    db.add(db_especie)
    db.commit()
    db.refresh(db_especie)
    return db_especie


def get_allEspecie(db: Session, skip=0, limit=100):
    especies = db.query(Especies).offset(skip).limit(limit).all()

    if not especies:
        raise HTTPException(
            status_code=404, detail="No existen especies en la base de datos")

    return especies


def get_especie(db: Session, especie_id: int):
    especie = db.query(Especies).filter(
        Especies.id == especie_id).first()

    if not especie:
        raise HTTPException(
            status_code=404, detail="La especie que marcó no está disponible")
    return especie


def create_mascota(db: Session, veterinaria_id: int, mascota_in: MascotaCreate, tutor_id: int):
    existe_tutor = get_tutor(db, tutor_id)

    veterinaria = get_veterinaria(db, veterinaria_id)

    db_mascota = Mascotas(
        name=mascota_in.name,
        description=mascota_in.description,
        birth_date=mascota_in.birth_date,
        tutor_id=tutor_id,
        especie_id=mascota_in.especie_id,
        veterinaria_id=veterinaria_id
    )

    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota


def get_mascota(db: Session, mascota_id: int):
    mascota = db.query(Mascotas).filter(
        Mascotas.id == mascota_id
    ).first()

    if not mascota:
        raise HTTPException(
            status_code=404,
            detail="Mascota no encontrada"
        )

    return mascota


def update_mascota(db: Session, mascota_id: int, mascota_in: MascotaUpdate):
    existe_mascota = get_mascota(db, mascota_id)

    update_data = mascota_in.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existe_mascota, field, value)

    try:
        db.commit()
        db.refresh(existe_mascota)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar la mascota"
        )

    return existe_mascota


def getall_mascota(db: Session, veterinaria_id: int, skip=0, limit=100):
    mascotas = db.query(Mascotas).filter(
        Mascotas.veterinaria_id == veterinaria_id
    ).offset(skip).limit(limit).all()

    if not mascotas:
        raise HTTPException(
            status_code=404,
            detail="No hay mascotas en esta veterinaria"
        )

    return mascotas


def delete_mascota(db: Session, mascota_id: int):
    mascota = get_mascota(db, mascota_id)

    try:
        db.delete(mascota)
        db.commit()
        db.refresh(mascota)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar la mascota"
        )

    return mascota
