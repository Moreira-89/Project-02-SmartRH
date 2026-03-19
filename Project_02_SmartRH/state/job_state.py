import reflex as rx
from typing import Optional
from Project_02_SmartRH.models.job import Job
from Project_02_SmartRH.services.firebase_service import FirebaseService


class JobFormState(rx.State):
    id: str = ""
    title: str = ""
    main_activity: str = ""
    prerequisites: str = ""
    differentials: Optional[str] = None
    status: str = "active"

    def salvar_vaga(self):
        
        nova_vaga = Job(
            id=self.id,
            title=self.title,
            main_activity=self.main_activity,
            prerequisites=self.prerequisites,
            differentials=self.differentials if self.differentials else None
        )
        FirebaseService().create_job(job=nova_vaga)