from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database, metadata

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Система Электронного Документооборота",
    description="API для управления документами и сотрудниками",
    openapi_tags=metadata.tags_metadata,
    version="1.0"
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Запросы для сотрудников
@app.post("/employees/", response_model=schemas.Employee, tags=["Сотрудники"])
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_emp = models.Employee(**employee.dict())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

@app.get("/employees/", response_model=List[schemas.Employee], tags=["Сотрудники"])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Employee).offset(skip).limit(limit).all()

# Запросы для входящих документов
@app.post("/incoming/", response_model=schemas.IncomingDocument, tags=["Входящие документы"])
def create_incoming(doc: schemas.IncomingDocumentCreate, db: Session = Depends(get_db)):
    db_doc = models.IncomingDocument(**doc.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@app.get("/incoming/", response_model=List[schemas.IncomingDocument], tags=["Входящие документы"])
def read_incoming(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.IncomingDocument).offset(skip).limit(limit).all()

# Запросы для исходящих документов
@app.post("/outgoing/", response_model=schemas.OutgoingDocument, tags=["Исходящие документы"])
def create_outgoing(doc: schemas.OutgoingDocumentCreate, db: Session = Depends(get_db)):
    db_doc = models.OutgoingDocument(**doc.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@app.get("/outgoing/", response_model=List[schemas.OutgoingDocument], tags=["Исходящие документы"])
def read_outgoing(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.OutgoingDocument).offset(skip).limit(limit).all()

# Запросы для служебных записок
@app.post("/memos/", response_model=schemas.Memo, tags=["Служебные записки"])
def create_memo(memo: schemas.MemoCreate, db: Session = Depends(get_db)):
    db_memo = models.Memo(**memo.dict())
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo

@app.get("/memos/", response_model=List[schemas.Memo], tags=["Служебные записки"])
def read_memos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Memo).offset(skip).limit(limit).all()

# Запросы для Отчетов
@app.post("/reports/", response_model=schemas.Report, tags=["Отчеты сотрудников"])
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    db_report = models.Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@app.get("/reports/", response_model=List[schemas.Report], tags=["Отчеты сотрудников"])
def read_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Report).offset(skip).limit(limit).all()

# Запросы для приказов
@app.post("/orders/", response_model=schemas.Order, tags=["Приказы"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/", response_model=List[schemas.Order], tags=["Приказы"])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Order).offset(skip).limit(limit).all()