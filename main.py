from routers import veterinaria, tutor, mascota, servicio, profesional, turno, libretaSanitaria, auth
from fastapi import FastAPI
from database.db import Base, engine


from models.models import Veterinarias, Tutores, Especies, Mascotas, Servicios, DetalleServicio, Turnos, LibretaSanitaria

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(veterinaria.router)
app.include_router(tutor.router)
app.include_router(mascota.router)
app.include_router(servicio.router)
app.include_router(profesional.router)
app.include_router(turno.router)
app.include_router(libretaSanitaria.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "API Veterinarias funcionando - Tablas creadas"}
