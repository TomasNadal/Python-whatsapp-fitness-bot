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
    email: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256), nullable=True)
    date_of_birth: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime(timezone=True), nullable=True)
    gender: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True)
    height: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, nullable=True)
    initial_weight: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, nullable=True)
    phone_number: so.Mapped[str] = so.mapped_column(sa.String(30), unique=True, nullable=False)
    state: so.Mapped[str] = so.mapped_column(sa.String, default="IdleState")
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True, nullable=False
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), index=True, nullable=False
    )
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50), nullable=True)
    surname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50), nullable=True)
    alias: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50), nullable=True)

    # Relationships
    training_sessions: so.Mapped[List['TrainingSession']] = so.relationship(
        'TrainingSession', back_populates='user', cascade='all, delete-orphan'
    )
    user_stats: so.Mapped[List['UserStats']] = so.relationship('UserStats', back_populates='user')

    def __repr__(self):
        return f'<User {self.phone_number}, {self.alias}>'

class TrainingSession(db.Model):
    __tablename__ = 'training_sessions'

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), nullable=False)
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
    ejercicio_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('exercises.id', name='fk_training_details_exercise'),
        nullable=False
    )
    atleta_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('users.id', name='fk_training_details_user'),
        nullable=False
    )
    hash_id: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), index=True
    )

    # Relationships
    session: so.Mapped['TrainingSession'] = so.relationship('TrainingSession', back_populates='training_details')
    atleta: so.Mapped['User'] = so.relationship('User', foreign_keys=[atleta_id])
    ejercicio: so.Mapped['Exercise'] = so.relationship('Exercise', back_populates='training_details')

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
            self.ejercicio_id == other.ejercicio_id and
            self.atleta_id == other.atleta_id and
            self.hash_id == other.hash_id and
            self.created_at == other.created_at and
            self.updated_at == other.updated_at
    )
    
class Exercise(db.Model):
    __tablename__ = 'exercises'

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)

    # Relationships
    training_details: so.Mapped[List['TrainingDetail']] = so.relationship('TrainingDetail', back_populates='ejercicio')
    user_stats: so.Mapped[List['UserStats']] = so.relationship('UserStats', back_populates='exercise')

class UserStats(db.Model):
    __tablename__ = 'user_stats'

    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('users.id', name='fk_user_stats_user'),
        primary_key=True
    )
    exercise_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('exercises.id', name='fk_user_stats_exercise'),
        primary_key=True
    )
    ecuacion: so.Mapped[str] = so.mapped_column(sa.JSON, nullable=False)
    
    # Relationships
    user: so.Mapped['User'] = so.relationship('User', back_populates='user_stats')
    exercise: so.Mapped['Exercise'] = so.relationship('Exercise', back_populates='user_stats')


