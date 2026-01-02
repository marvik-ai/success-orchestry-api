from typing import List
from app.Models.SeniorityModel import Seniority, SeniorityCreate
from app.Database.Repositories.SeniorityRepository import SeniorityRepositoryClass

class SeniorityService:
    def __init__(self, seniority_repo: SeniorityRepositoryClass) -> None:
        self.seniority_repo = seniority_repo

    def get_all(self) -> List[Seniority]:
        return self.seniority_repo.get()

    def add(self, seniority: SeniorityCreate) -> Seniority:
        return self.seniority_repo.add(seniority)
