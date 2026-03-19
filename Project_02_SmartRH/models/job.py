from pydantic import BaseModel
from typing import Optional, List

class Job(BaseModel):
    id: str
    title: str
    main_activity: str
    prerequisites: str
    differentials: Optional[str] = None
    status: str = "active"