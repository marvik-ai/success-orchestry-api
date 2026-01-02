from fastapi import APIRouter, Depends, HTTPException
from app.Models.ClientModel import Client
# Import the dependency FUNCTION, not the class directly
from app.dependencies import get_clients_services, ClientService 

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=Client)
def create_new_client(
    client: Client, 
    service: ClientService = Depends(get_clients_services)
):
    return service.create(client)

@router.get("/", response_model=list[Client])
def list_clients(
    service: ClientService = Depends(get_clients_services)
):
    return service.getAll()

@router.patch("/{clientCode}", response_model=Client)
def edit_client(
    clientCode: str, 
    client: Client, 
    service: ClientService = Depends(get_clients_services)
):
    updated = service.edit(clientCode, client)
    if not updated:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return updated

@router.get("/{clientCode}", response_model=Client)
def getClient( clientCode: str, service:ClientService = Depends(get_clients_services)):
    return service.getClient(clientCode)
