from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text, Index, CheckConstraint, UniqueConstraint

from sqlalchemy.orm import relationship, declarative_base

from sqlalchemy.ext.declarative import declared_attr

import datetime
from sqlalchemy import Boolean

from database.db import Base


class TimestampMixin:

    created_at = Column(

        DateTime, default=datetime.datetime.utcnow, nullable=False)

    updated_at = Column(DateTime, default=datetime.datetime.utcnow,

                        onupdate=datetime.datetime.utcnow, nullable=False)


class VeterinariaMixin:

    @declared_attr
    def veterinaria_id(cls):

        return Column(Integer, ForeignKey('veterinarias.id'), nullable=False)

    @declared_attr
    def veterinaria(cls):

        return relationship("Veterinarias")


class Veterinarias(Base, TimestampMixin):

    __tablename__ = "veterinarias"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)

    phone = Column(String(20))

    address = Column(Text)

    is_active = Column(Boolean, default=True)

    mascotas = relationship(

        "Mascotas", back_populates="veterinaria", cascade="all, delete-orphan")

    profesionales = relationship(

        "Profesionales", back_populates="veterinaria", cascade="all, delete-orphan")

    tutores = relationship("Tutores", back_populates="veterinaria")

    servicios = relationship("Servicios", back_populates="veterinaria")

    def __repr__(self):

        return f"<Veterinaria(id={self.id}, name='{self.name}')>"


class Tutores(Base, TimestampMixin, VeterinariaMixin):

    __tablename__ = "tutores"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    email = Column(String(100), nullable=False)

    phone = Column(String(20))

    address = Column(Text)

    mascotas = relationship(

        "Mascotas", back_populates="tutor", cascade="all, delete-orphan")

    veterinaria = relationship("Veterinarias", back_populates="tutores")

    def __repr__(self):

        return f"<Tutor(id={self.id}, name='{self.name}')>"


class Especies(Base, TimestampMixin):

    __tablename__ = "especies"

    id = Column(Integer, primary_key=True)

    nombre = Column(String(50), unique=True, nullable=False)

    descripcion = Column(Text)

    is_active = Column(Integer, default=1)

    mascotas = relationship("Mascotas", back_populates="especie")

    def __repr__(self):

        return f"<Especie(id={self.id}, nombre='{self.nombre}')>"


class Mascotas(Base, TimestampMixin, VeterinariaMixin):

    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    birth_date = Column(Date)

    especie_id = Column(Integer, ForeignKey('especies.id'), nullable=False)

    color = Column(String(50))

    description = Column(Text)

    tutor_id = Column(Integer, ForeignKey('tutores.id'), nullable=False)

    tutor = relationship("Tutores", back_populates="mascotas")

    especie = relationship("Especies", back_populates="mascotas")

    turnos = relationship("Turnos", back_populates="mascota",

                          cascade="all, delete-orphan")

    libreta_sanitaria = relationship(

        "LibretaSanitaria", back_populates="mascota", cascade="all, delete-orphan")

    __table_args__ = (

        Index('ix_mascotas_tutor', 'tutor_id'),

        Index('ix_mascotas_especie', 'especie_id'),

        Index('ix_mascotas_veterinaria', 'veterinaria_id'),

    )

    def __repr__(self):

        return f"<Mascota(id={self.id}, name='{self.name}', especie={self.especie_id})>"


class Profesionales(Base, TimestampMixin, VeterinariaMixin):

    __tablename__ = "profesionales"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    email = Column(String(100))

    phone = Column(String(20))

    specialty = Column(String(100))

    is_active = Column(Integer, default=1)

    veterinaria = relationship("Veterinarias", back_populates="profesionales")

    detalle_servicios = relationship(

        "DetalleServicio", back_populates="profesional", cascade="all, delete-orphan")

    libretas_sanitarias = relationship(

        "LibretaSanitaria", back_populates="profesional")

    def __repr__(self):

        return f"<Profesional(id={self.id}, name='{self.name}')>"


class Servicios(Base, TimestampMixin, VeterinariaMixin):

    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    description = Column(Text)

    is_active = Column(Integer, default=1)

    detalle_servicios = relationship(

        "DetalleServicio", back_populates="servicio", cascade="all, delete-orphan")

    veterinaria = relationship("Veterinarias", back_populates="servicios")

    def __repr__(self):

        return f"<Servicio(id={self.id}, name='{self.name}')>"


class DetalleServicio(Base, TimestampMixin, VeterinariaMixin):

    __tablename__ = "detalles_servicio"

    id = Column(Integer, primary_key=True)

    servicio_id = Column(Integer, ForeignKey('servicios.id'), nullable=False)

    profesional_id = Column(Integer, ForeignKey(

        'profesionales.id'), nullable=False)

    servicio = relationship("Servicios", back_populates="detalle_servicios")

    profesional = relationship(

        "Profesionales", back_populates="detalle_servicios")

    turnos = relationship(

        "Turnos", back_populates="detalle_servicio", cascade="all, delete-orphan")

    def __repr__(self):

        return f"<DetalleServicio(id={self.id}, servicio={self.servicio_id})>"


class EstadoTurno(Base, TimestampMixin):

    __tablename__ = "estados_turno"

    id = Column(Integer, primary_key=True)

    nombre = Column(String(50), unique=True, nullable=False)

    descripcion = Column(Text)

    # Relaciones

    turnos = relationship("Turnos", back_populates="estado")

    def __repr__(self):

        return f"<EstadoTurno(id={self.id}, nombre='{self.nombre}')>"


class Turnos(Base, TimestampMixin, VeterinariaMixin):

    __tablename__ = "turnos"

    id = Column(Integer, primary_key=True)

    fecha_hora = Column(DateTime, nullable=False)

    mascota_id = Column(Integer, ForeignKey('mascotas.id'), nullable=False)

    detalle_servicio_id = Column(Integer, ForeignKey(

        'detalles_servicio.id'), nullable=False)

    estado_id = Column(Integer, ForeignKey(

        'estados_turno.id'), nullable=False, default=1)

    notes = Column(Text)

    mascota = relationship("Mascotas", back_populates="turnos")

    detalle_servicio = relationship("DetalleServicio", back_populates="turnos")

    estado = relationship("EstadoTurno", back_populates="turnos")

    veterinaria = relationship("Veterinarias")

    # Índices y constraints

    __table_args__ = (

        Index('ix_turnos_fecha_hora', 'fecha_hora'),

        Index('ix_turnos_mascota_estado', 'mascota_id', 'estado_id'),

        Index('ix_turnos_veterinaria', 'veterinaria_id'),

        # Prevenir doble booking

        UniqueConstraint('fecha_hora', 'detalle_servicio_id',

                         name='uq_turno_servicio_fecha'),

    )

    def __repr__(self):

        return f"<Turno(id={self.id}, fecha_hora='{self.fecha_hora}', mascota={self.mascota_id})>"


class LibretaSanitaria(Base, TimestampMixin, VeterinariaMixin):

    __tablename__ = "libretas_sanitarias"

    id = Column(Integer, primary_key=True)

    mascota_id = Column(Integer, ForeignKey('mascotas.id'), nullable=False)

    profesional_id = Column(Integer, ForeignKey(

        'profesionales.id'), nullable=False)

    vacuna = Column(String(100), nullable=False)

    fecha_vacunacion = Column(Date, nullable=False)

    fecha_proxima_dosis = Column(Date)

    observaciones = Column(Text)

    # Relaciones

    mascota = relationship("Mascotas", back_populates="libreta_sanitaria")

    profesional = relationship(

        "Profesionales", back_populates="libretas_sanitarias")

    veterinaria = relationship("Veterinarias")

    __table_args__ = (

        Index('ix_libreta_mascota', 'mascota_id'),

        Index('ix_libreta_profesional', 'profesional_id'),

        Index('ix_libreta_fecha_vacunacion', 'fecha_vacunacion'),

    )

    def __repr__(self):

        return f"<LibretaSanitaria(id={self.id}, mascota={self.mascota_id}, vacuna='{self.vacuna}')>"
