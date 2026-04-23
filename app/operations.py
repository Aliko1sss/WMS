from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product, Operation
from app.schemas import OperationCreate

router = APIRouter(prefix="/operations", tags=["operations"])

# Бизнес-логика (для Unit-тестов)
def calculate_stock(current: float, op_type: str, amount: float) -> float:
    if amount <= 0:
        raise ValueError("Количество должно быть > 0")
    if op_type == "IN":
        return current + amount
    elif op_type == "OUT":
        if current < amount:
            raise ValueError("Недостаточно товара на складе")
        return current - amount
    else:
        raise ValueError("Недопустимый тип операции (IN/OUT)")

@router.post("/", status_code=200)
def create_operation(op: OperationCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == op.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    try:
        new_quantity = calculate_stock(product.quantity, op.op_type, op.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    product.quantity = new_quantity
    
    db_op = Operation(product_id=op.product_id, op_type=op.op_type, amount=op.amount)
    db.add(db_op)
    db.commit()
    
    return {"status": "ok", "new_quantity": new_quantity}