from fastapi import FastAPI
from app.routes import dcrm

app = FastAPI(
    title = "DCRM anomaly detection API",
    description="API for detecting anomalies in DCRM data using machine learning models.",
    version="1.0.0"
)

app.include_router(dcrm.router, prefix="/dcrm", tags=["DCRM"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the DCRM anomaly detection API!"}