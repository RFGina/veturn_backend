from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    auth,
    veterinaria,
    tutor,
    mascota,
    servicio,
    profesional,
    turno,
    libretaSanitaria,
)

app = FastAPI(
    title="Veturn API",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(veterinaria.router)
app.include_router(tutor.router)
app.include_router(mascota.router)
app.include_router(servicio.router)
app.include_router(profesional.router)
app.include_router(turno.router)
app.include_router(libretaSanitaria.router)


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok"}
