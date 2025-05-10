from pydantic import BaseModel
from datetime import datetime

class Resume(BaseModel):
    id: str
    job_id: str
    candidate_name: str
    file_url: str
    file_type: str
    file_size: str
    upload_date: str = datetime.now().isoformat()
    status: str = "pending"