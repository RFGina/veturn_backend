from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.models import Servicios
from database.db import get_db
from schemas.servicio import ServicioCreate, ServicioUpdate, ServicioOut, DetalleServicioCreate, DetalleServicioOut, DetalleServicioUpdate
from crud.servicio import (
    createServicio,
    getServicio,
    updateServicio,
    getAllServicios,
    get_detalle_servicio_veterinaria,
    get_detalles_servicio_veterinaria,
    createDetServicio,
    updateDetServicio
)
from models.models import Veterinarias
from auth.jwt import get_current_veterinaria

router = APIRouter(
    prefix="/servicios",
    tags=["servicios"]
)


@router.get("/{servicio_id}/ver_servicio", response_model=ServicioOut)
def ver_servicio(servicio_id: int, db: Session = Depends(get_db)):
    return getServicio(db, servicio_id)


@router.get("/lista_servicios", response_model=list[ServicioOut])
def listar_servicios(
        skip=0,
        limit=100,
        current_vet: Veterinarias = Depends(get_current_veterinaria),
        db: Session = Depends(get_db)):
    return getAllServicios(db, current_vet.id, skip, limit)


@router.post("/crear_servicio", response_model=ServicioOut)
def crear_servicio(servicio: ServicioCreate, current_vet: Veterinarias = Depends(get_current_veterinaria), db: Session = Depends(get_db)):
    return createServicio(db, servicio, current_vet.id)


@router.put("/{servicio_id}/editar_servicio", response_model=ServicioOut)
def editar_servicio(servicio_id: int, servicio: ServicioUpdate, db: Session = Depends(get_db)):
    return updateServicio(db, servicio, servicio_id)


@router.get("/detalles_servicio", response_model=list[DetalleServicioOut])
def getDetalles(id_veterinaria: int, current_dv: Veterinarias = Depends(get_current_veterinaria), db: Session = Depends(get_db)):
    return get_detalles_servicio_veterinaria(db, current_dv.id)


@router.get("/{dServicio_id}/detalle_servicio", response_model=DetalleServicioOut)
def get_detalle_servicio(dServicio_id: int, db: Session = Depends(get_db)):
    return get_detalle_servicio_veterinaria(db, dServicio_id)


@router.post("/crear_detalle_servicio", response_model=DetalleServicioOut)
def crear_dServicio(detalle_in: DetalleServicioCreate, current_dv: Veterinarias = Depends(get_current_veterinaria), db: Session = Depends(get_db)):
    return createDetServicio(db, detalle_in, current_dv.id)


@router.put("/{dservicio_id}/edit_detalle_servicio", response_model=DetalleServicioOut)
def editar_dServicio(detalle_in: DetalleServicioUpdate, dservicio_id: int, db: Session = Depends(get_db)):
    return updateDetServicio(db, detalle_in, dservicio_id)
