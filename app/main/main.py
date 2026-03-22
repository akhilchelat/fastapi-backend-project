from fastapi import FastAPI
from app.routes import user, employee,department, analytics

from app.db.base import Base
from app.db.session import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(employee.router)
app.include_router(department.router)
app.include_router(analytics.router)