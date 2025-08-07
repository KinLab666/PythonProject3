from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Сотрудник
class EmployeeBase(BaseModel):
    full_name: str
    position: str
    email: str
    phone: Optional[str] = None
    note: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    full_name: Optional[str] = None
    position: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    note: Optional[str] = None

class Employee(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Входящие документы
class IncomingDocumentBase(BaseModel):
    sender_id: str
    subject: str
    resolution: Optional[str] = None
    note: Optional[str] = None

class IncomingDocumentCreate(IncomingDocumentBase):
    pass

class IncomingDocumentUpdate(IncomingDocumentBase):
    sender_id: Optional[int] = None
    subject: Optional[str] = None
    resolution: Optional[str] = None
    note: Optional[str] = None

class IncomingDocument(IncomingDocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Исходящие документы
class OutgoingDocumentBase(BaseModel):
    recipient_id: str
    subject: str
    delivery_method: str  # "email" or "mail"
    note: Optional[str] = None

class OutgoingDocumentCreate(OutgoingDocumentBase):
    pass

class OutgoingDocumentUpdate(OutgoingDocumentBase):
    recipient_id: Optional[int] = None
    subject: Optional[str] = None
    delivery_method: Optional[str] = None
    note: Optional[str] = None

class OutgoingDocument(OutgoingDocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Служебные записки
class MemoBase(BaseModel):
    author_id: int
    content: str
    note: Optional[str] = None

class MemoCreate(MemoBase):
    pass

class MemoUpdate(MemoBase):
    author_id: Optional[int] = None
    content: Optional[str] = None
    note: Optional[str] = None

class Memo(MemoBase):
    id: int
    author: Employee
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Отчеты
class ReportBase(BaseModel):
    author_id: int
    note: Optional[str] = None

class ReportCreate(ReportBase):
    pass

class ReportUpdate(ReportBase):
    author_id: Optional[int] = None
    note: Optional[str] = None

class Report(ReportBase):
    id: int
    author: Employee
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Приказы
class OrderBase(BaseModel):
    content: str
    signer_id: int
    note: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    content: Optional[str] = None
    signer_id: Optional[int] = None
    note: Optional[str] = None

class Order(OrderBase):
    id: int
    signer: Employee
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True