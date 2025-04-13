from pydantic import BaseModel


class ResumUseCase(BaseModel):
    id: str
    job_id: str
    content: str
    model_opinion: str
    file: str
