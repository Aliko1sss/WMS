from pydantic import BaseModel, ConfigDict

class ProductCreate(BaseModel):
    sku: str
    name: str
    quantity: float = 0.0

class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    sku: str
    name: str
    quantity: float

class OperationCreate(BaseModel):
    product_id: int
    op_type: str
    amount: float