from app.Models.RoleModel import Role, RoleCreate
from app.Database.Repositories.RolesRepository import RoleRepositoryClass
from typing import List

class RoleService:
    def __init__(self, role_repo: RoleRepositoryClass):
        self.role_repo = role_repo

    def get_all(self) -> List[Role]:
        roles = self.role_repo.get()
        return roles

    def add(self, role : RoleCreate):
        added_role = self.role_repo.add(role)
        return added_role
