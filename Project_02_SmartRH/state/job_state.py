import reflex as rx
import uuid
from Project_02_SmartRH.models.job import Job
from Project_02_SmartRH.services.firebase_service import FirebaseService


class JobFormState(rx.State):
    id: str = ""
    title: str = ""
    main_activity: str = ""
    prerequisites: str = ""
    differentials: str = ""
    status: str = "active"

    def salvar_vaga(self):
        self.id = str(uuid.uuid4())
        nova_vaga = Job(
            id=self.id,
            title=self.title,
            main_activity=self.main_activity,
            prerequisites=self.prerequisites,
            differentials=self.differentials if self.differentials else None
        )
        FirebaseService().create_job(job=nova_vaga)
        rx.toast.success("Vaga criada com sucesso!", duration=3000)
        self.title = ""
        self.main_activity = ""
        self.prerequisites = ""
        self.differentials = ""
