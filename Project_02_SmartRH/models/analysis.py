from pydantic import BaseModel
from typing import List, Optional


class Analysis(BaseModel):
    id: str
    job_id: str
    resume_id: str
    job_title: Optional[str] = None
    name: str
    skills: List[str]
    education: List[str]
    languages: List[str]
    score: float