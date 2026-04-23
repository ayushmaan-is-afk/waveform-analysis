from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.prediction import predict_dcrm
from app.services.preprocessing import data_preprocessing
import pandas as pd
import tempfile
import os
from pathlib import Path

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    #Making sure that the uploaded file(s) are only CSV(s)
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Only CSV files accepted")
    
    try:
        # Saving temp file in the server for processing and predicting
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        
        # Preprocessing the data
        df = data_preprocessing(Path(tmp_path))
        
        # Predicting
        result = predict_dcrm(df)
        
        # Cleanup
        os.unlink(tmp_path)
        
        return {
            "filename"        : file.filename,
            "scores"          : result['scores mean'],
            "status"          : result['status'],
            "severity"        : result['severity'],
            "anomaly_score"   : result['anomaly_score'],
            "anomaly_percent" : result['anomaly_percent']
        }
    except Exception as e:
        os.unlink(tmp_path) if "tmp_path" in locals() else None
        raise HTTPException(500, f"Prediction failed: {str(e)}")

@router.get("/health")
def health_check():
    return {"status": "ok", "message": "DCRM prediction service is running"}