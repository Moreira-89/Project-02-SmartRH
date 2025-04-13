from pydantic import BaseModel
from typing import List

class CurriculumAnalysisUseCase(BaseModel):
    id: str
    job_id: str
    content: str
    resume_id: str
    name: str
    skills: List[str]
    education: List[str]
    languages: List[str]
    score: float
