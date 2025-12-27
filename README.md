## `Veturn Backend` – API de Gestión de Veterinarias

## 🔹 Descripción

`Veturn Backend` es un **backend RESTful** desarrollado en **Python + FastAPI + SQLAlchemy**, diseñado para gestionar veterinarias, tutores, mascotas, profesionales, servicios y turnos.

El sistema implementa relaciones complejas, mixins para timestamps, validaciones, constraints y manejo seguro de passwords

## 🔹 Stack Tecnológico

* **Lenguaje:** Python 
* **Framework:** FastAPI
* **ORM:** SQLAlchemy
* **Base de Datos:** SQLite 
* **Seguridad:** PassLib + Bcrypt para hashed passwords
* **Gestión de dependencias:** Poetry / pip
* **Documentación:** FastAPI OpenAPI (Swagger UI)

---

## 🔹 Funcionalidades

* CRUD completo para:

  * Veterinarias
  * Tutores
  * Mascotas
  * Profesionales
  * Servicios y Detalles de Servicios
  * Turnos y Estados de Turnos
  * Libretas Sanitarias
* Relaciones entre entidades:

  * Una veterinaria tiene múltiples tutores, mascotas, servicios y profesionales.
  * Mascotas pertenecen a tutores y tienen especie definida.
  * Turnos vinculados a servicios, profesionales y mascotas.
  * Una mascota vinculada a una libreta sanitaria
* Seguridad:

  * Passwords hash con bcrypt
* Validaciones y manejo de errores con HTTPException
* Indexes y constraints para integridad y performance

---

## 🔹 Estructura del Proyecto

```
veturn_backend/
|-auth/                  #jwt, passlib
|-crud/                 # Funciones CRUD por entidad
|- database/             # Configuración DB y Base
|- helpers/            #por ahora vacio(solo timezone)
|- models/               # SQLAlchemy models
|- routers/              # Endpoints FastAPI por recurso
|- schemas/              # Pydantic schemas
|-main.py               # Entrada principal de FastAPI            
|- requirements.txt      # Dependencias
|- README.md             # Documentación
```

---

## 🔹 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/RFGina/veturn_backend.git
cd veturn_backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---

## 🔹 Levantar la API

```bash
uvicorn main:app --reload
```

* La API estará disponible en `http://127.0.0.1:8000`
* Documentación automática en `http://127.0.0.1:8000/docs` (Swagger UI)

---

## 🔹 Endpoints Ejemplo

### Crear Veterinaria

```bash
POST /veterinarias/
{
  "name": "Vet1",
  "email": "vet1@mail.com",
  "password": "123456",
  "phone": "123456789",
  "address": "Calle Falsa 123"
}
```

### Obtener Mascotas por Veterinaria

```bash
GET /mascotas/?veterinaria_id=1
```

### Crear Turno

```bash
POST /turnos/
{
  "fecha_hora": "2025-12-30T10:00:00",
  "mascota_id": 1,
  "detalle_servicio_id": 2,
  "estado_id": 1,
  "notes": "Chequeo anual"
}
```

### Respuesta ejemplo (GET `/mascotas/`)

```json
[
  {
    "id": 1,
    "name": "Firulais",
    "especie": "Perro",
    "tutor": "Juan Perez",
    "veterinaria": "Vet1",
    "birth_date": "2020-05-01"
  }
]
```

---

