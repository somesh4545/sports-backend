from fastapi import FastAPI

from routes.index import userRouter
from routes.index import studentsRouter
from routes.index import organizerssRouter

from config.db import get_db, engine
import models.index as models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def backend_testing():
    return {'msg', 'backend is running'}

# app.include_router(userRouter, prefix='/user')
app.include_router(studentsRouter, prefix='/student')
app.include_router(organizerssRouter, prefix='/organizer')