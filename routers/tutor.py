from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import Veterinarias
from auth.jwt import get_current_veterinaria
from database.db import get_db
from schemas.tutor import TutorCreate, TutorOut, TutorUpdate
from crud.tutor import (
    create_tutor,
    get_tutor,
    get_tutores,
    delete_tutor,
    get_tutor_by_email,
    update_tutor
)

router = APIRouter(
    prefix="/tutores",
    tags=["tutores"]
)


@router.post("/crear_tutor", response_model=TutorOut, status_code=201)
def create(tutor: TutorCreate, current_vet: Veterinarias = Depends(get_current_veterinaria),  db: Session = Depends(get_db)):
    existing = get_tutor_by_email(db, tutor.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado"
        )

    return create_tutor(db, tutor, current_vet.id)


@router.get("/ver_tutores", response_model=list[TutorOut])
def read_all(skip: int = 0, limit: int = 100, current_vet: Veterinarias = Depends(get_current_veterinaria), db: Session = Depends(get_db)):
    return get_tutores(db, current_vet.id, skip=skip, limit=limit)


@router.get("/{tutor_id}", response_model=TutorOut)
def read_one(tutor_id: int, db: Session = Depends(get_db)):
    return get_tutor(db, tutor_id)


@router.delete("/{tutor_id}", response_model=TutorOut)
def delete(tutor_id: int, db: Session = Depends(get_db)):
    tutor = delete_tutor(db, tutor_id)

    if not tutor:
        raise HTTPException(
            status_code=404,
            detail="No se pudo eliminar el tutor"
        )

    return tutor


@router.put("/{tutor_id}/editar", response_model=TutorOut)
def update_tutor_endpoint(tutor_id: int, tutor: TutorUpdate, db: Session = Depends(get_db)):
    return update_tutor(db, tutor_id, tutor)
