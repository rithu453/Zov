from fastapi import FastAPI
from app.routes import dashboard_r,record_r,user_r
from app.db.database import engine, Base
from app.models import user_model,record_model


app= FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(user_r.router, prefix="/users", tags=["users"] )
app.include_router(record_r.router, prefix="/records", tags=["records"])
app.include_router(dashboard_r.router, prefix="/dashboard" ,tags=["dashboard"])

@app.get("/")
def root():
    return { "message" : "Finance backend is running"}

