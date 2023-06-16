from fastapi import FastAPI

from routes.index import userRouter
from routes.index import studentsRouter, organizerssRouter, adminsRouter, tournamentsRouter, teamsRouter

from config.db import get_db, engine
import models.index as models
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*","http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def backend_testing():
    return {'msg', 'backend is running'}

# app.include_router(userRouter, prefix='/user')
app.include_router(studentsRouter, prefix='/student')
app.include_router(organizerssRouter, prefix='/organizer')
app.include_router(tournamentsRouter, prefix='/tournament')
app.include_router(teamsRouter, prefix='/team')

app.include_router(adminsRouter, prefix='/admin')