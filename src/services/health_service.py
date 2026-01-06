from sqlmodel import Session, select


class HealthService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def check(self) -> dict[str, str]:
        # Usamos select(1) que devuelve un objeto Select,
        # compatible con session.exec() y el tipado de MyPy.
        self.session.exec(select(1))
        return {'status': 'ok'}
