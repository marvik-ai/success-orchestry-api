from sqlmodel import Session, select
from app.Models.ClientModel import Client

class ClientRepositoryClass:
    def __init__(self, session : Session):
        self.session = session

    def create_client(self, client_data: Client):
        # Validate and create the DB instance
        db_client = Client.model_validate(client_data)
        self.session.add(db_client)
        self.session.commit()
        self.session.refresh(db_client)
        return db_client

    def get_all_clients(self):
        # Fetch all clients from the table
        return self.session.exec(select(Client)).all()

    def get_client_by_code(self, client_code: str):
        # Find a specific client by its unique code
        statement = select(Client).where(Client.client_code == client_code)
        return self.session.exec(statement).first()

    def update_client(self, db_client: Client, new_data: Client):
        # Convert new data to a dict, ignoring fields not provided
        client_data_dict = new_data.model_dump(exclude_unset=True)
        
        for key, value in client_data_dict.items():
            if key != "id": # ID must never be changed
                setattr(db_client, key, value)
        
        self.session.add(db_client)
        self.session.commit()
        self.session.refresh(db_client)
        return db_client
