from pydantic import BaseModel
from typing import Optional, List

class PredictionResponse(BaseModel):
    status:str
    anomaly_score: float
    anomaly_percentage: float
    faulty_components: Optional[dict]
    maintenance_recs : Optional[dict]
    
class HealthCheckResponse(BaseModel):
    status  : str
    message : str