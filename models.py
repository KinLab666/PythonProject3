from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    note = Column(Text, nullable=True)

    memos = relationship("Memo", back_populates="author")
    reports = relationship("Report", back_populates="author")
    orders = relationship("Order", back_populates="signer")

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class IncomingDocument(Base):
    __tablename__ = "incoming_documents"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(String(200), nullable=False)
    subject = Column(String(200), nullable=False)
    resolution = Column(Text, nullable=True)
    note = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class OutgoingDocument(Base):
    __tablename__ = "outgoing_documents"

    id = Column(Integer, primary_key=True, index=True)
    recipient_id = Column(String(200), nullable=False)
    subject = Column(String(200), nullable=False)
    delivery_method = Column(Enum("email", "mail", name="delivery_method"), nullable=False)
    note = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Memo(Base):
    __tablename__ = "memos"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    content = Column(Text, nullable=False)
    note = Column(Text, nullable=True)

    author = relationship("Employee", back_populates="memos")

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    note = Column(Text, nullable=False)

    author = relationship("Employee", back_populates="reports")

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    signer_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    note = Column(Text, nullable=True)

    signer = relationship("Employee", back_populates="orders")

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)