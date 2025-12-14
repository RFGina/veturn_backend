from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from database.db import get_db
from crud.libretaSanitaria import (
    createLibreta,
    getAll_libreta,
    get_libreta,
    updateLibreta
)
from models.models import Veterinarias
from auth.jwt import get_current_veterinaria
from schemas.libretaSanitaria import (
    LibretaCreate,
    LibretaOut,
    LibretaUpdate
)

router = APIRouter(
    prefix="/libretaSanitaria",
    tags=["libretas"]
)


@router.get("/ver_libretas", response_model=LibretaOut)
def ver_libretas(current_dv: Veterinarias = Depends(get_current_veterinaria), db: Session = Depends(get_db)):
    return getAll_libreta(db, current_dv.id)


@router.get("/{libreta_id}/ver_libreta", response_model=LibretaOut)
def ver_libreta(libreta_id: int, db: Session = Depends(get_db)):
    return get_libreta(db, libreta_id)


@router.post("/crear_libreta/", response_model=LibretaOut)
def crear_libreta(libreta_in: LibretaCreate, current_dv: Veterinarias = Depends(get_current_veterinaria), db: Session = Depends(get_db)):
    return createLibreta(db, libreta_in, current_dv.id)


@router.put("/{libreta_id}/editar_libreta", response_model=LibretaOut)
def editar_libreta(libreta_id: int, libreta_in: LibretaUpdate, db: Session = Depends(get_db)):
    return updateLibreta(db, libreta_in, libreta_id)
