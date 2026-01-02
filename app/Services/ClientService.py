from fastapi import HTTPException
from app.Models.ClientModel import Client
from app.Database.Repositories import ClientRepository

class ClientService:
    def __init__(self, cli_repo : ClientRepository):
        self.cli_repo = cli_repo
         
    def getAll(self):
        return self.cli_repo.get_all_clients()

    def create(self, client: Client):
        # Use the lookup helper for uniqueness validation
        existing = self.cli_repo.get_client_by_code(client.client_code)
        if existing:
            raise HTTPException(status_code=400, detail="Code already exists")
        return self.cli_repo.create_client(client)

    def edit(self, client_code: str, client_data: Client):
        db_client = self.cli_repo.get_client_by_code(client_code)
        if not db_client:
            return None
        return self.cli_repo.update_client(db_client, client_data)

    def getClient(self,client_code:str):
        db_client = self.cli_repo.get_client_by_code(client_code)
        if not db_client:
            return None
        return db_client
