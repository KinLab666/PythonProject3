from fastapi import FastAPI, Depends, HTTPException
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

def get_or_404(db, model, item_id: int):
    item = db.query(model).filter(model.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"{model.__name__} с id={item_id} не найден")
    return item

# Запросы для сотрудников
@app.post("/employees/", response_model=schemas.Employee, tags=["Сотрудники"], summary = "Создание сотрудника")
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_emp = models.Employee(**employee.dict())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

@app.get("/employees/", response_model=List[schemas.Employee], tags=["Сотрудники"], summary = "Просмотр списка сотрудников")
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Employee).offset(skip).limit(limit).all()

@app.put("/employees/{emp_id}", response_model=schemas.Employee, tags=["Сотрудники"], summary = "Редактирование сотрудника")
def update_employee(emp_id: int, data: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    emp = get_or_404(db, models.Employee, emp_id)
    for key, value in data.dict().items():
        setattr(emp, key, value)
    db.commit()
    db.refresh(emp)
    return emp

@app.patch("/employees/{emp_id}", response_model=schemas.Employee, tags=["Сотрудники"], summary = "Частичное редактирование сотрудника")
def partial_update_employee(emp_id: int, data: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    emp = get_or_404(db, models.Employee, emp_id)
    for key, value in data.dict(exclude_unset=True).items():
        if value is not None:
            setattr(emp, key, value)
    db.commit()
    db.refresh(emp)
    return emp

@app.delete("/employees/{emp_id}", tags=["Сотрудники"], summary = "Удаление сотрудника")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = get_or_404(db, models.Employee, emp_id)
    db.delete(emp)
    db.commit()
    return {"detail": f"Сотрудник с id={emp_id} успешно удалён"}

# Запросы для входящих документов
@app.post("/incoming/", response_model=schemas.IncomingDocument, tags=["Входящие документы"], summary = "Создание входящего документа")
def create_incoming(doc: schemas.IncomingDocumentCreate, db: Session = Depends(get_db)):
    db_doc = models.IncomingDocument(**doc.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@app.get("/incoming/", response_model=List[schemas.IncomingDocument], tags=["Входящие документы"], summary = "Просмотр списка входящих документов")
def read_incoming(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.IncomingDocument).offset(skip).limit(limit).all()

@app.put("/incoming/{doc_id}", response_model=schemas.IncomingDocument, tags=["Входящие документы"], summary = "Редактирование входящего документа")
def update_incoming(doc_id: int, data: schemas.IncomingDocumentUpdate, db: Session = Depends(get_db)):
    doc = get_or_404(db, models.IncomingDocument, doc_id)
    for key, value in data.dict().items():
        setattr(doc, key, value)
    db.commit()
    db.refresh(doc)
    return doc

@app.patch("/incoming/{doc_id}", response_model=schemas.IncomingDocument, tags=["Входящие документы"], summary = "Частичное редактирование входящего документа")
def partial_update_incoming(doc_id: int, data: schemas.IncomingDocumentUpdate, db: Session = Depends(get_db)):
    doc = get_or_404(db, models.IncomingDocument, doc_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(doc, key, value)
    db.commit()
    db.refresh(doc)
    return doc

@app.delete("/incoming/{doc_id}", tags=["Входящие документы"], summary = "Удаление входящего документа")
def delete_incoming(doc_id: int, db: Session = Depends(get_db)):
    doc = get_or_404(db, models.IncomingDocument, doc_id)
    db.delete(doc)
    db.commit()
    return {"detail": f"Входящий документ с id={doc_id} удалён"}

# Запросы для исходящих документов
@app.post("/outgoing/", response_model=schemas.OutgoingDocument, tags=["Исходящие документы"], summary = "Создание исходящего документа")
def create_outgoing(doc: schemas.OutgoingDocumentCreate, db: Session = Depends(get_db)):
    db_doc = models.OutgoingDocument(**doc.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@app.get("/outgoing/", response_model=List[schemas.OutgoingDocument], tags=["Исходящие документы"], summary = "Просмотр списка исходящих документов")
def read_outgoing(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.OutgoingDocument).offset(skip).limit(limit).all()

@app.put("/outgoing/{doc_id}", response_model=schemas.OutgoingDocument, tags=["Исходящие документы"], summary = "Редактирование исходящего документа")
def update_outgoing(doc_id: int, data: schemas.OutgoingDocumentUpdate, db: Session = Depends(get_db)):
    doc = get_or_404(db, models.OutgoingDocument, doc_id)
    if data.delivery_method and data.delivery_method not in ["email", "mail"]:
        raise HTTPException(status_code=400, detail="delivery_method: 'email' или 'mail'")
    for key, value in data.dict().items():
        setattr(doc, key, value)
    db.commit()
    db.refresh(doc)
    return doc

@app.patch("/outgoing/{doc_id}", response_model=schemas.OutgoingDocument, tags=["Исходящие документы"], summary = "Частичное редактирование исходящего документа")
def partial_update_outgoing(doc_id: int, data: schemas.OutgoingDocumentUpdate, db: Session = Depends(get_db)):
    doc = get_or_404(db, models.OutgoingDocument, doc_id)
    update_data = data.dict(exclude_unset=True)
    if "delivery_method" in update_data and update_data["delivery_method"] not in ["email", "mail"]:
        raise HTTPException(status_code=400, detail="delivery_method: 'email' или 'mail'")
    for key, value in update_data.items():
        setattr(doc, key, value)
    db.commit()
    db.refresh(doc)
    return doc

@app.delete("/outgoing/{doc_id}", tags=["Исходящие документы"], summary = "Удаление исходящего документа")
def delete_outgoing(doc_id: int, db: Session = Depends(get_db)):
    doc = get_or_404(db, models.OutgoingDocument, doc_id)
    db.delete(doc)
    db.commit()
    return {"detail": f"Исходящий документ с id={doc_id} удалён"}

# Запросы для служебных записок
@app.post("/memos/", response_model=schemas.Memo, tags=["Служебные записки"], summary = "Создание служебной записки")
def create_memo(memo: schemas.MemoCreate, db: Session = Depends(get_db)):
    db_memo = models.Memo(**memo.dict())
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo

@app.get("/memos/", response_model=List[schemas.Memo], tags=["Служебные записки"], summary = "Просмотр списка служебных записок")
def read_memos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Memo).offset(skip).limit(limit).all()

@app.put("/memos/{memo_id}", response_model=schemas.Memo, tags=["Служебные записки"], summary = "Редактирование служебной записки")
def update_memo(memo_id: int, data: schemas.MemoUpdate, db: Session = Depends(get_db)):
    memo = get_or_404(db, models.Memo, memo_id)
    for key, value in data.dict().items():
        setattr(memo, key, value)
    db.commit()
    db.refresh(memo)
    return memo

@app.patch("/memos/{memo_id}", response_model=schemas.Memo, tags=["Служебные записки"], summary = "Частичное редактирование служебной записки")
def partial_update_memo(memo_id: int, data: schemas.MemoUpdate, db: Session = Depends(get_db)):
    memo = get_or_404(db, models.Memo, memo_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(memo, key, value)
    db.commit()
    db.refresh(memo)
    return memo

@app.delete("/memos/{memo_id}", tags=["Служебные записки"], summary = "Удаление служебной записки")
def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    memo = get_or_404(db, models.Memo, memo_id)
    db.delete(memo)
    db.commit()
    return {"detail": f"Служебная записка с id={memo_id} удалена"}

# Запросы для Отчетов
@app.post("/reports/", response_model=schemas.Report, tags=["Отчеты сотрудников"], summary = "Создание отчета сотрудника")
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    db_report = models.Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@app.get("/reports/", response_model=List[schemas.Report], tags=["Отчеты сотрудников"], summary = "Просмотр списка отчетов сотрудников")
def read_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Report).offset(skip).limit(limit).all()

@app.put("/reports/{report_id}", response_model=schemas.Report, tags=["Отчеты сотрудников"], summary = "Редактирование отчета сотрудника")
def update_report(report_id: int, data: schemas.ReportUpdate, db: Session = Depends(get_db)):
    report = get_or_404(db, models.Report, report_id)
    for key, value in data.dict().items():
        setattr(report, key, value)
    db.commit()
    db.refresh(report)
    return report

@app.patch("/reports/{report_id}", response_model=schemas.Report, tags=["Отчеты сотрудников"], summary = "Частичное редактирование отчета сотрудника")
def partial_update_report(report_id: int, data: schemas.ReportUpdate, db: Session = Depends(get_db)):
    report = get_or_404(db, models.Report, report_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(report, key, value)
    db.commit()
    db.refresh(report)
    return report

@app.delete("/reports/{report_id}", tags=["Отчеты сотрудников"], summary = "Удаление отчета сотрудника")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    report = get_or_404(db, models.Report, report_id)
    db.delete(report)
    db.commit()
    return {"detail": f"Отчёт с id={report_id} удалён"}

# Запросы для приказов
@app.post("/orders/", response_model=schemas.Order, tags=["Приказы"], summary = "Создание приказа")
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/", response_model=List[schemas.Order], tags=["Приказы"], summary = "Просмотр списка приказов")
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Order).offset(skip).limit(limit).all()

@app.put("/orders/{order_id}", response_model=schemas.Order, tags=["Приказы"], summary = "Редактирование приказа")
def update_order(order_id: int, data: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order = get_or_404(db, models.Order, order_id)
    for key, value in data.dict().items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order

@app.patch("/orders/{order_id}", response_model=schemas.Order, tags=["Приказы"], summary = "Частичное редактирование приказа")
def partial_update_order(order_id: int, data: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order = get_or_404(db, models.Order, order_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order

@app.delete("/orders/{order_id}", tags=["Приказы"], summary = "Удаление приказа")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = get_or_404(db, models.Order, order_id)
    db.delete(order)
    db.commit()
    return {"detail": f"Приказ с id={order_id} удалён"}