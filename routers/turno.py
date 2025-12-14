from sqlalchemy.orm import Session
from models.models import Veterinarias
from auth.jwt import get_current_veterinaria
from fastapi import APIRouter, Depends
from database.db import get_db
from schemas.turno import (
    EstadoTurnoCreate,
    EstadoTurnoOut,
    TurnoOut,
    TurnoCreate,
    TurnoUpdate
)
from crud.turno import getAllTurnos, getTurno, updateTurno, crearTurno, crearEstadoTurno, EstadoTurnoCreate, get_estados

router = APIRouter(
    prefix="/turnos",
    tags=["turnos"]
)


@router.post("/crear_estado", response_model=EstadoTurnoOut)
def crear_turno(estado_in: EstadoTurnoCreate, db: Session = Depends(get_db)):
    return crearEstadoTurno(db, estado_in)


@router.post("/crear_turno", response_model=TurnoOut)
def crear_turno(turno_in: TurnoCreate, current_vet: Veterinarias = Depends(get_current_veterinaria), db: Session = Depends(get_db)):
    return crearTurno(db, turno_in, current_vet.id)


@router.get("/obtener_estado", response_model=list[EstadoTurnoOut])
def ver_estados(skip=0, limit=0, db: Session = Depends(get_db)):
    return get_estados(db, skip, limit)


@router.get("/ver_turnos", response_model=list[TurnoOut])
def ver_turnos(current_vet: Veterinarias = Depends(get_current_veterinaria), db: Session = Depends(get_db)):
    return getAllTurnos(db, current_vet.id)


@router.get("/{turno_id}/ver_turno", response_model=TurnoOut)
def ver_turno(turno_id: int, db: Session = Depends(get_db)):
    return getTurno(turno_id, db)


@router.put("/{turno_id}/editar_turno")
def editar_turno(turno_id, turno_in: TurnoUpdate, db: Session = Depends(get_db)):
    return updateTurno(db, turno_in, turno_id)
