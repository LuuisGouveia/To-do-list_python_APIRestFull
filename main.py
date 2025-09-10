from fastapi import FastAPI
from app import models, database, routes


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="To-Do List API")

app.include_router(routes.router)