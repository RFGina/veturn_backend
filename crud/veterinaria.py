from sqlalchemy.orm import Session
from models.models import Veterinarias
from schemas.veterinaria import VeterinariaCreate, VeterinariaUpdate
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_veterinaria(db: Session, veterinaria_in: VeterinariaCreate):
    hashed_password = get_password_hash(veterinaria_in.password)

    db_veterinaria = Veterinarias(
        name=veterinaria_in.name,
        email=veterinaria_in.email,
        hashed_password=hashed_password,
        phone=veterinaria_in.phone,
        address=veterinaria_in.address
    )

    db.add(db_veterinaria)
    db.commit()
    db.refresh(db_veterinaria)

    return db_veterinaria


def get_veterinaria(db: Session, veterinaria_id: int):
    vet = db.query(Veterinarias).filter(
        Veterinarias.id == veterinaria_id).first()

    if not vet:
        raise HTTPException("No existe la veterinaria.")
    return vet


def get_veterinaria_by_email(db: Session, email: str):
    return db.query(Veterinarias).filter(Veterinarias.email == email).first()


def get_veterinarias(db: Session, skip=0, limit=100):
    print(" Ejecutando consulta de veterinarias...")

    resultado = db.query(Veterinarias).offset(skip).limit(limit).all()

    print(f"SQLAlchemy encontró: {len(resultado)} registros")

    for i, vet in enumerate(resultado):
        print(f"  {i+1}. ID: {vet.id}, Name: {vet.name}, Email: {vet.email}")
        print(f"     Tipo: {type(vet)}, Atributos: {vars(vet)}")

    return resultado


def update_veterinaria(db: Session, veterinaria_id: int, usuario_in: VeterinariaUpdate):
    db_vet = db.query(Veterinarias).filter(
        Veterinarias.id == veterinaria_id).first()

    if not db_vet:
        raise HTTPException(
            status_code=404, detail="Veterinaria no encontrada")

    update_data = usuario_in.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_vet, field, value)

    db.commit()
    db.refresh(db_vet)

    return db_vet


def delete_veterinaria(db: Session, user_id: int):
    veterinaria = get_veterinaria(db, user_id)
    if veterinaria:
        db.delete(veterinaria)
        db.commit()
    return veterinaria
