from pydantic import BaseModel


class FileUseCase(BaseModel):
    file_id: str
    job_id: str
    