from fastapi import FastAPI
from database import engine, Base
from routers import workouts, auth
import model
Base.metadata.create_all(bind=engine)
app=FastAPI()
app.include_router(workouts.router)
app.include_router(auth.router)