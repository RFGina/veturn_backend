from sqlalchemy.orm import Session, joinedload
from models.models import Servicios, DetalleServicio, Profesionales
from fastapi import HTTPException
from schemas.servicio import ServicioCreate, ServicioUpdate, DetalleServicioCreate, DetalleServicioUpdate
from .veterinaria import get_veterinaria
from .profesional import get_prof, getall_prof


def getAllServicios(db: Session, veterinaria_id: int, skip=0, limit=100):
    servicios = db.query(Servicios).filter(
        Servicios.veterinaria_id == veterinaria_id).offset(skip).limit(limit).all()

    if not servicios:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron servicios"
        )

    return servicios


def getServicio(db: Session, servicio_id: int):
    servicio = db.query(Servicios).filter(Servicios.id == servicio_id).first()

    if not servicio:
        raise HTTPException(
            status_code='404',
            detail='No se encontro el servicio que seleccionó'
        )

    return servicio


def createServicio(db: Session, servicio_in: ServicioCreate, veterinaria_id: int):
    get_veterinaria(db, veterinaria_id)

    db_servicio = Servicios(
        name=servicio_in.name,
        description=servicio_in.description,
        veterinaria_id=veterinaria_id
    )

    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)

    return db_servicio


def updateServicio(db: Session, servicio_in: ServicioUpdate, servicio_id: int):
    servicio = getServicio(db, servicio_id)

    update_data = servicio_in.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(servicio, field, value)

    try:
        db.commit()
        db.refresh(servicio)
    except Exception:
        raise HTTPException(
            status_code="500",
            detail="Error al actualizar el servicio"
        )

    return servicio


def deleteServicio(db: Session, servicio_id: int):
    servicio = getServicio(db, servicio_id)

    try:
        db.delete(servicio)
        db.commit()
        db.refresh(servicio)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar el servicio"
        )

    return servicio


def createDetServicio(db: Session, detalle_in: DetalleServicioCreate, id_veterinaria: int):

    servicioD = DetalleServicio(
        servicio_id=detalle_in.servicio_id,
        profesional_id=detalle_in.profesional_id,
        veterinaria_id=id_veterinaria
    )

    db.add(servicioD)
    db.commit()
    db.refresh(servicioD)

    return servicioD


def get_detalles_servicio_veterinaria(db: Session, veterinaria_id: int):
    detalles = db.query(
        DetalleServicio,
        Servicios.name.label("nombre_servicio"),
        Profesionales.name.label("nombre_profesional")
    )\
        .join(Servicios, DetalleServicio.servicio_id == Servicios.id)\
        .join(Profesionales, DetalleServicio.profesional_id == Profesionales.id)\
        .filter(Servicios.veterinaria_id == veterinaria_id)\
        .all()

    if not detalles:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron los servicios"
        )

    resultado = []
    for detalle, nombre_servicio, nombre_profesional in detalles:
        detalle_dict = {
            "id": detalle.id,
            "servicio_id": detalle.servicio_id,
            "nombre_servicio": nombre_servicio,
            "profesional_id": detalle.profesional_id,
            "nombre_profesional": nombre_profesional,
            "veterinaria_id": detalle.veterinaria_id,
            "created_at": detalle.created_at,
            "updated_at": detalle.updated_at
        }
        resultado.append(detalle_dict)

    return resultado


def get_detalle_servicio_veterinaria(db: Session, dServicio_id: int):
    resultado = db.query(
        DetalleServicio,
        Servicios.name.label("nombre_servicio"),
        Profesionales.name.label("nombre_profesional")
    )\
        .join(Servicios, DetalleServicio.servicio_id == Servicios.id)\
        .join(Profesionales, DetalleServicio.profesional_id == Profesionales.id)\
        .filter(DetalleServicio.id == dServicio_id)\
        .first()

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el detalle de servicio"
        )

    detalle, nombre_servicio, nombre_profesional = resultado

    return {
        "id": detalle.id,
        "servicio_id": detalle.servicio_id,
        "nombre_servicio": nombre_servicio,
        "profesional_id": detalle.profesional_id,
        "nombre_profesional": nombre_profesional,
        "veterinaria_id": detalle.veterinaria_id,
        "created_at": detalle.created_at,
        "updated_at": detalle.updated_at
    }


def updateDetServicio(db: Session, detalle_in: DetalleServicioUpdate, dservicio_id: int):
    serviciod = get_detalle_servicio_veterinaria(db, dservicio_id)

    update_s = detalle_in.dict(exclude_unset=True)

    for field, value in update_s.items():
        setattr(serviciod, field, value)

    try:
        db.commit()
        db.refresh(serviciod)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code="500",
            detail="No se pudo actualizar los datos"
        )
    return serviciod


def deleteServicioD(db: Session, dservicio_id: int):
    servicioD = get_detalle_servicio_veterinaria(db, dservicio_id)

    try:
        db.delete(servicioD)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar el profesional"
        )

    return {"message": "Servicio eliminado correctamente"}
