from auth.jwt import get_current_veterinaria
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from schemas.veterinaria import VeterinariaCreate, VeterinariaOut
from crud.veterinaria import (
    create_veterinaria,
    get_veterinaria,
    get_veterinarias,
    delete_veterinaria,
    get_veterinaria_by_email
)
from models.models import Veterinarias

router = APIRouter(
    prefix="/veterinarias",
    tags=["Veterinarias"]
)


@router.post("/", response_model=VeterinariaOut, status_code=201)
def create(veterinaria: VeterinariaCreate, db: Session = Depends(get_db)):
    existing = get_veterinaria_by_email(db, veterinaria.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado"
        )

    return create_veterinaria(db, veterinaria)


@router.get("/", response_model=list[VeterinariaOut])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_veterinarias(db, skip=skip, limit=limit)


@router.get("/me", response_model=VeterinariaOut)
def read_my_account(current_vet: Veterinarias = Depends(get_current_veterinaria)):
    return current_vet


@router.delete("/me", response_model=VeterinariaOut)
def delete_my_account(current_vet: Veterinarias = Depends(get_current_veterinaria),
                      db: Session = Depends(get_db)):
    return delete_veterinaria(db, current_vet.id)
