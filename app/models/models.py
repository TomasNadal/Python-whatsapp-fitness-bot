# app/models.py

from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.types import DateTime
from app import db
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=False)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256), nullable=True)
    date_of_birth: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), nullable=False)
    gender: so.Mapped[str] = so.mapped_column(sa.String(20), nullable=False)
    height: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    initial_weight: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    phone_number: so.Mapped[str] = so.mapped_column(sa.String(30), nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True, nullable=False
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), index=True, nullable=False
    )
    
    # Nuevos Campos Opcionales
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50), nullable=True)
    surname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50), nullable=True)
    alias: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50), nullable=True)

    # Relationships
    training_sessions: so.Mapped[List['TrainingSession']] = so.relationship(
        'TrainingSession', back_populates='user', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<User {self.phone_number}, {self.alias}>'

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return (
            self.id == other.id and
            self.email == other.email and
            self.password_hash == other.password_hash and
            self.date_of_birth == other.date_of_birth and
            self.gender == other.gender and
            self.height == other.height and
            self.initial_weight == other.initial_weight and
            self.phone_number == other.phone_number and
            self.created_at == other.created_at and
            self.updated_at == other.updated_at and
            self.name == other.name and
            self.surname == other.surname and
            self.alias == other.alias
        )


class TrainingSession(db.Model):
    __tablename__ = 'training_sessions'

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), nullable=False)
    # Have to delete this date
    date: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), nullable=False)
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), index=True
    )

    # Relationships
    user: so.Mapped['User'] = so.relationship('User', back_populates='training_sessions')
    training_details: so.Mapped[List['TrainingDetail']] = so.relationship(
        'TrainingDetail', back_populates='session', cascade='all, delete-orphan'
    )

    def __eq__(self, other):
        if not isinstance(other, TrainingSession):
            return False
        return (
            self.id == other.id and
            self.user_id == other.user_id and
            self.date == other.date and
            self.notes == other.notes and
            self.created_at == other.created_at and
            self.updated_at == other.updated_at
        )


class TrainingDetail(db.Model):
    __tablename__ = 'training_details'

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    session_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('training_sessions.id'), nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    serie: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    rep: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    kg: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    d: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, nullable=True)
    vm: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, nullable=True)
    vmp: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, nullable=True)
    rm: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    p_w: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, nullable=True)
    perfil: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    ejercicio: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    ecuacion: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    atleta_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), nullable=False)
    hash_id: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), index=True
    )

    # Relationships
    session: so.Mapped['TrainingSession'] = so.relationship('TrainingSession', back_populates='training_details')
    atleta: so.Mapped['User'] = so.relationship('User')

    def __eq__(self, other):
        if not isinstance(other, TrainingDetail):
            return False
        return (
            self.id == other.id and
            self.session_id == other.session_id and
            self.timestamp == other.timestamp and
            self.serie == other.serie and
            self.rep == other.rep and
            self.kg == other.kg and
            self.d == other.d and
            self.vm == other.vm and
            self.vmp == other.vmp and
            self.rm == other.rm and
            self.p_w == other.p_w and
            self.perfil == other.perfil and
            self.ejercicio == other.ejercicio and
            self.ecuacion == other.ecuacion and
            self.atleta_id == other.atleta_id and
            self.hash_id == other.hash_id and
            self.created_at == other.created_at and
            self.updated_at == other.updated_at
        )
