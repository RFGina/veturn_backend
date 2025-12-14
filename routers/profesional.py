from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from database.db import get_db
from schemas.profesional import ProfesionalCreate, ProfesionalUpdate, ProfesionalOut
from crud.profesional import (
    getall_prof,
    get_prof,
    create_profesional,
    update_profesional
)
from models.models import Veterinarias
from auth.jwt import get_current_veterinaria

router = APIRouter(
    prefix="/profesionales",
    tags=["profesionales"]
)


@router.get("/listar_profesionales", response_model=list[ProfesionalOut])
def getAllProfesionales(skip=0, limit=0, db: Session = Depends(get_db), current_dv: Veterinarias = Depends(get_current_veterinaria)):
    return getall_prof(db, current_dv.id, skip, limit)


@router.get("/{profesional_id}/ver_profesional", response_model=ProfesionalOut)
def getProfesionales(profesional_id: int, db: Session = Depends(get_db)):
    return get_prof(db, profesional_id)


@router.post("/crear_profesional", response_model=ProfesionalOut)
def crearProfesional(profesional: ProfesionalCreate, current_dv: Veterinarias = Depends(get_current_veterinaria), db: Session = Depends(get_db)):
    return create_profesional(db, profesional, current_dv.id)


@router.put("/{profesional_id}/editar_profesional", response_model=ProfesionalOut)
def editar_profesiona(profesional_id: int, profesional: ProfesionalUpdate, db: Session = Depends(get_db)):
    return update_profesional(db, profesional_id, profesional)
