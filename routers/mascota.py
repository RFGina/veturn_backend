from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import Mascotas
from database.db import get_db
from schemas.mascota import MascotaCreate, MascotaUpdate, MascotaOut, EspecieOut, EspecieCreate
from crud.mascota import (
    create_especies,
    create_mascota,
    get_especie,
    get_allEspecie,
    get_mascota,
    getall_mascota,
    update_mascota,
    delete_mascota
)
from models.models import Veterinarias
from auth.jwt import get_current_veterinaria

router = APIRouter(
    prefix="/mascotas",
    tags=["mascotas"]
)


@router.get("/especies/", response_model=list[EspecieOut])
def ver_especies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_allEspecie(db, skip=skip, limit=limit)


@router.get("{especie_id}/especies/", response_model=EspecieOut)
def ver_especies(especie_id: int, db: Session = Depends(get_db)):
    return get_allEspecie(db, especie_id)


@router.post("/crear_especie/", response_model=EspecieOut)
def crear_especie(especie: EspecieCreate, db: Session = Depends(get_db)):
    return create_especies(db, especie)


@router.post("/tutores/{tutor_id}/mascotas")
def crear_mascota(tutor_id: int, mascota_in: MascotaCreate, db: Session = Depends(get_db), current_dv: Veterinarias = Depends(get_current_veterinaria)):
    return create_mascota(db, current_dv.id, mascota_in, tutor_id)


@router.get("/listar_mascotas", response_model=list[MascotaOut])
def listar_mascota(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_dv: Veterinarias = Depends(get_current_veterinaria)):
    return getall_mascota(db, current_dv.id, skip, limit)


@router.get("/{mascota_id}/ver_mascota", response_model=MascotaOut)
def ver_mascota(mascota_id: int, db: Session = Depends(get_db)):
    return get_mascota(db, mascota_id)


@router.put("/{mascota_id}/editar_mascota", response_model=MascotaOut)
def editar_mascota(mascota_id: int, mascota: MascotaUpdate, db: Session = Depends(get_db)):
    return update_mascota(db, mascota_id, mascota)
