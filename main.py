from fastapi import FastAPI, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database, metadata

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Система Электронного Документооборота",
    description="это веб-приложение на Python, реализованное с использованием фреймворка FastAPI, предназначенное для автоматизации управления документами в организации.",
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
@app.post("/employees/", response_model=schemas.Employee, tags=["Сотрудники"], summary = metadata.summary_emp1, description=metadata.summary_emp1, response_description=metadata.response_description1)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_emp = models.Employee(**employee.model_dump())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

@app.get("/employees/",response_model=List[schemas.Employee], tags=["Сотрудники"], summary = metadata.summary_emp2, description=metadata.summary_emp2, response_description=metadata.response_description1)
def read_employees(
        skip: int = Query(0, description=metadata.query_description1),
        limit: int = Query(100, description=metadata.query_description2),
        db: Session = Depends(get_db)):
    return db.query(models.Employee).offset(skip).limit(limit).all()

@app.put("/employees/{emp_id}", response_model=schemas.Employee, tags=["Сотрудники"], summary = metadata.summary_emp3, description=metadata.summary_emp3, response_description=metadata.response_description1)
def update_employee(
        data: schemas.EmployeeUpdate,
        emp_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    emp = get_or_404(db, models.Employee, emp_id)
    for key, value in data.model_dump().items():
        setattr(emp, key, value)
    db.commit()
    db.refresh(emp)
    return emp

@app.patch("/employees/{emp_id}", response_model=schemas.Employee, tags=["Сотрудники"], summary = metadata.summary_emp4, description=metadata.summary_emp4, response_description=metadata.response_description1)
def partial_update_employee(
        data: schemas.EmployeeUpdate,
        emp_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    emp = get_or_404(db, models.Employee, emp_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(emp, key, value)
    db.commit()
    db.refresh(emp)
    return emp

@app.delete("/employees/{emp_id}", tags=["Сотрудники"], summary = metadata.summary_emp5, description=metadata.summary_emp5)
def delete_employee(
        emp_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    emp = get_or_404(db, models.Employee, emp_id)
    db.delete(emp)
    db.commit()
    return {"detail": f"Сотрудник с id={emp_id} успешно удалён"}

# Запросы для входящих документов
@app.post("/incoming/", response_model=schemas.IncomingDocument, tags=["Входящие документы"], summary = metadata.summary_inc1, description=metadata.summary_inc1, response_description=metadata.response_description2)
def create_incoming(doc: schemas.IncomingDocumentCreate, db: Session = Depends(get_db)):
    db_doc = models.IncomingDocument(**doc.model_dump())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@app.get("/incoming/", response_model=List[schemas.IncomingDocument], tags=["Входящие документы"], summary = metadata.summary_inc2, description=metadata.summary_inc2, response_description=metadata.response_description2)
def read_incoming(
        skip: int = Query(0, description=metadata.query_description1),
        limit: int = Query(100, description=metadata.query_description2),
        db: Session = Depends(get_db)):
    return db.query(models.IncomingDocument).offset(skip).limit(limit).all()

@app.put("/incoming/{doc_id}", response_model=schemas.IncomingDocument, tags=["Входящие документы"], summary = metadata.summary_inc3, description=metadata.summary_inc3, response_description=metadata.response_description2)
def update_incoming(
        data: schemas.IncomingDocumentUpdate,
        doc_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    doc = get_or_404(db, models.IncomingDocument, doc_id)
    for key, value in data.model_dump().items():
        setattr(doc, key, value)
    db.commit()
    db.refresh(doc)
    return doc

@app.patch("/incoming/{doc_id}", response_model=schemas.IncomingDocument, tags=["Входящие документы"], summary = metadata.summary_inc4, description=metadata.summary_inc4, response_description=metadata.response_description2)
def partial_update_incoming(
        data: schemas.IncomingDocumentUpdate,
        doc_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    doc = get_or_404(db, models.IncomingDocument, doc_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(doc, key, value)
    db.commit()
    db.refresh(doc)
    return doc

@app.delete("/incoming/{doc_id}", tags=["Входящие документы"], summary = metadata.summary_inc5, description=metadata.summary_inc5)
def delete_incoming(
        doc_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    doc = get_or_404(db, models.IncomingDocument, doc_id)
    db.delete(doc)
    db.commit()
    return {"detail": f"Входящий документ с id={doc_id} удалён"}

# Запросы для исходящих документов
@app.post("/outgoing/", response_model=schemas.OutgoingDocument, tags=["Исходящие документы"], summary = metadata.summary_out1, description=metadata.summary_out1, response_description=metadata.response_description3)
def create_outgoing(doc: schemas.OutgoingDocumentCreate, db: Session = Depends(get_db)):
    db_doc = models.OutgoingDocument(**doc.model_dump())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@app.get("/outgoing/", response_model=List[schemas.OutgoingDocument], tags=["Исходящие документы"], summary = metadata.summary_out2, description=metadata.summary_out2, response_description=metadata.response_description3)
def read_outgoing(
        skip: int = Query(0, description=metadata.query_description1),
        limit: int = Query(100, description=metadata.query_description2),
        db: Session = Depends(get_db)):
    return db.query(models.OutgoingDocument).offset(skip).limit(limit).all()

@app.put("/outgoing/{doc_id}", response_model=schemas.OutgoingDocument, tags=["Исходящие документы"], summary = metadata.summary_out3, description=metadata.summary_out3, response_description=metadata.response_description3)
def update_outgoing(
        data: schemas.OutgoingDocumentUpdate,
        doc_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    doc = get_or_404(db, models.OutgoingDocument, doc_id)
    if data.delivery_method and data.delivery_method not in ["email", "mail"]:
        raise HTTPException(status_code=400, detail="delivery_method: 'email' или 'mail'")
    for key, value in data.model_dump().items():
        setattr(doc, key, value)
    db.commit()
    db.refresh(doc)
    return doc

@app.patch("/outgoing/{doc_id}", response_model=schemas.OutgoingDocument, tags=["Исходящие документы"], summary = metadata.summary_out4, description=metadata.summary_out4, response_description=metadata.response_description3)
def partial_update_outgoing(
        data: schemas.OutgoingDocumentUpdate,
        doc_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    doc = get_or_404(db, models.OutgoingDocument, doc_id)
    update_data = data.model_dump(exclude_unset=True)
    if "delivery_method" in update_data and update_data["delivery_method"] not in ["email", "mail"]:
        raise HTTPException(status_code=400, detail="delivery_method: 'email' или 'mail'")
    for key, value in update_data.items():
        setattr(doc, key, value)
    db.commit()
    db.refresh(doc)
    return doc

@app.delete("/outgoing/{doc_id}", tags=["Исходящие документы"], summary = metadata.summary_out5, description=metadata.summary_out5)
def delete_outgoing(
        doc_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    doc = get_or_404(db, models.OutgoingDocument, doc_id)
    db.delete(doc)
    db.commit()
    return {"detail": f"Исходящий документ с id={doc_id} удалён"}

# Запросы для служебных записок
@app.post("/memos/", response_model=schemas.Memo, tags=["Служебные записки"], summary = metadata.summary_memo1, description=metadata.summary_memo1, response_description=metadata.response_description4)
def create_memo(memo: schemas.MemoCreate, db: Session = Depends(get_db)):
    db_memo = models.Memo(**memo.model_dump())
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo

@app.get("/memos/", response_model=List[schemas.Memo], tags=["Служебные записки"], summary = metadata.summary_memo2, description=metadata.summary_memo2, response_description=metadata.response_description4)
def read_memos(
        skip: int = Query(0, description=metadata.query_description1),
        limit: int = Query(100, description=metadata.query_description2),
        db: Session = Depends(get_db)):
    return db.query(models.Memo).offset(skip).limit(limit).all()

@app.put("/memos/{memo_id}", response_model=schemas.Memo, tags=["Служебные записки"], summary = metadata.summary_memo3, description=metadata.summary_memo3, response_description=metadata.response_description4)
def update_memo(
        data: schemas.MemoUpdate,
        memo_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    memo = get_or_404(db, models.Memo, memo_id)
    for key, value in data.model_dump().items():
        setattr(memo, key, value)
    db.commit()
    db.refresh(memo)
    return memo

@app.patch("/memos/{memo_id}", response_model=schemas.Memo, tags=["Служебные записки"], summary = metadata.summary_memo4, description=metadata.summary_memo4, response_description=metadata.response_description4)
def partial_update_memo(
        data: schemas.MemoUpdate,
        memo_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    memo = get_or_404(db, models.Memo, memo_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(memo, key, value)
    db.commit()
    db.refresh(memo)
    return memo

@app.delete("/memos/{memo_id}", tags=["Служебные записки"], summary = metadata.summary_memo5, description=metadata.summary_memo5)
def delete_memo(
        memo_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    memo = get_or_404(db, models.Memo, memo_id)
    db.delete(memo)
    db.commit()
    return {"detail": f"Служебная записка с id={memo_id} удалена"}

# Запросы для Отчетов
@app.post("/reports/", response_model=schemas.Report, tags=["Отчеты сотрудников"], summary = metadata.summary_rep1, description=metadata.summary_rep1, response_description=metadata.response_description5)
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    db_report = models.Report(**report.model_dump())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@app.get("/reports/", response_model=List[schemas.Report], tags=["Отчеты сотрудников"], summary = metadata.summary_rep2, description=metadata.summary_rep2, response_description=metadata.response_description5)
def read_reports(
        skip: int = Query(0, description=metadata.query_description1),
        limit: int = Query(100, description=metadata.query_description2),
        db: Session = Depends(get_db)):
    return db.query(models.Report).offset(skip).limit(limit).all()

@app.put("/reports/{report_id}", response_model=schemas.Report, tags=["Отчеты сотрудников"], summary = metadata.summary_rep3, description=metadata.summary_rep3, response_description=metadata.response_description5)
def update_report(
        data: schemas.ReportUpdate,
        report_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    report = get_or_404(db, models.Report, report_id)
    for key, value in data.model_dump().items():
        setattr(report, key, value)
    db.commit()
    db.refresh(report)
    return report

@app.patch("/reports/{report_id}", response_model=schemas.Report, tags=["Отчеты сотрудников"], summary = metadata.summary_rep4, description=metadata.summary_rep4, response_description=metadata.response_description5)
def partial_update_report(
        data: schemas.ReportUpdate,
        report_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    report = get_or_404(db, models.Report, report_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(report, key, value)
    db.commit()
    db.refresh(report)
    return report

@app.delete("/reports/{report_id}", tags=["Отчеты сотрудников"], summary = metadata.summary_rep5, description=metadata.summary_rep5)
def delete_report(
        report_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    report = get_or_404(db, models.Report, report_id)
    db.delete(report)
    db.commit()
    return {"detail": f"Отчёт с id={report_id} удалён"}

# Запросы для приказов
@app.post("/orders/", response_model=schemas.Order, tags=["Приказы"], summary = metadata.summary_ord1, description=metadata.summary_ord1, response_description=metadata.response_description6)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/", response_model=List[schemas.Order], tags=["Приказы"], summary = metadata.summary_ord2, description=metadata.summary_ord2, response_description=metadata.response_description6)
def read_orders(
        skip: int = Query(0, description=metadata.query_description1),
        limit: int = Query(100, description=metadata.query_description2),
        db: Session = Depends(get_db)):
    return db.query(models.Order).offset(skip).limit(limit).all()

@app.put("/orders/{order_id}", response_model=schemas.Order, tags=["Приказы"], summary = metadata.summary_ord3, description=metadata.summary_ord3, response_description=metadata.response_description6)
def update_order(
        data: schemas.OrderUpdate,
        order_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    order = get_or_404(db, models.Order, order_id)
    for key, value in data.model_dump().items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order

@app.patch("/orders/{order_id}", response_model=schemas.Order, tags=["Приказы"], summary = metadata.summary_ord4, description=metadata.summary_ord4, response_description=metadata.response_description6)
def partial_update_order(
        data: schemas.OrderUpdate,
        order_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    order = get_or_404(db, models.Order, order_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order

@app.delete("/orders/{order_id}", tags=["Приказы"], summary = metadata.summary_ord5, description=metadata.summary_ord5)
def delete_order(
        order_id: int = Path(..., description=metadata.query_description3),
        db: Session = Depends(get_db)):
    order = get_or_404(db, models.Order, order_id)
    db.delete(order)
    db.commit()
    return {"detail": f"Приказ с id={order_id} удалён"}