from pydantic import BaseModel, Field
from typing import Optional


class JobsUseCase(BaseModel):
    id: str
    name: str = Field(..., min_length=3)
    main_activities: str
    prerequisites: str
    differences: Optional[str] = None
    salary: float = Field(..., gt=0)
    location: str
    benefits: Optional[str] = None
