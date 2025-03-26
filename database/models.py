from sqlalchemy import (
    Column, Integer, String, DateTime, 
    ForeignKey, Enum, Boolean, Text,
    UniqueConstraint
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from database.db_connector import Base
import enum
import re
from datetime import datetime
import bcrypt

# Enums for constrained choices
class ThreatLevel(enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class UserRole(enum.Enum):
    ADMIN = "Administrator"
    SUPERVISOR = "Security Supervisor"
    OFFICER = "Security Officer"
    AUDITOR = "Compliance Auditor"

# Core Models
class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('username', name='uq_username'),
        UniqueConstraint('email', name='uq_email'),
    )

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    personnel = relationship("SecurityPersonnel", back_populates="user", uselist=False)
    reported_threats = relationship("Threat", back_populates="reporter")

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email.lower()

    def set_password(self, password):
        """Hash and store password"""
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, password):
        """Verify password against hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

class SecurityPersonnel(Base):
    __tablename__ = 'security_personnel'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    badge_number = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    clearance_level = Column(Integer, default=1)
    department = Column(String(50))
    hire_date = Column(DateTime, server_default=func.now())
    is_armed = Column(Boolean, default=False)
    certifications = Column(Text)

    # Relationships
    user = relationship("User", back_populates="personnel")
    assigned_threats = relationship("Threat", back_populates="assigned_officer")

class Threat(Base):
    __tablename__ = 'threats'

    id = Column(Integer, primary_key=True)
    reporter_id = Column(Integer, ForeignKey('users.id'))
    assigned_officer_id = Column(Integer, ForeignKey('security_personnel.id'))
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(100), nullable=False)
    threat_level = Column(Enum(ThreatLevel), nullable=False)
    status = Column(String(30), default='Reported')
    is_confirmed = Column(Boolean, default=False)
    reported_at = Column(DateTime, server_default=func.now())
    resolved_at = Column(DateTime)
    evidence_photos = Column(Text)  # JSON paths to files

    # Relationships
    reporter = relationship("User", back_populates="reported_threats")
    assigned_officer = relationship("SecurityPersonnel", back_populates="assigned_threats")
    audit_logs = relationship("AuditLog", back_populates="threat")

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    threat_id = Column(Integer, ForeignKey('threats.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(50), nullable=False)
    details = Column(Text)
    ip_address = Column(String(45))
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    threat = relationship("Threat", back_populates="audit_logs")
    user = relationship("User")

class SecurityCheckpoint(Base):
    __tablename__ = 'security_checkpoints'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    location = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    last_inspection = Column(DateTime)
    required_clearance = Column(Integer, default=1)
    equipment = Column(Text)  # JSON list of equipment
