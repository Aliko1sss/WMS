from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.products import router as products_router
from app.operations import router as operations_router

# ✅ Современный способ: lifespan-контекст
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, который выполняется при запуске
    Base.metadata.create_all(bind=engine)
    yield
    # Код, который выполняется при завершении (если нужно)

app = FastAPI(title="WMS MVP", lifespan=lifespan)

app.include_router(products_router)
app.include_router(operations_router)