from fastapi import FastAPI

from app.routes import user, employee,department, analytics


app = FastAPI()

app.include_router(user.router)
app.include_router(employee.router)
app.include_router(department.router)
app.include_router(analytics.router)