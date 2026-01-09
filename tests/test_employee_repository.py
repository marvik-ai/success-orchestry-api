from datetime import datetime
from uuid import uuid4

from sqlmodel import Session

from models.employee_model import Employee, EmployeePersonalInfo, EmployeeStatus
from repositories.employee_repository import EmployeeRepositoryClass


def test_repo_soft_delete_mixed_strategy(session: Session) -> None:
    # --- ARRANGE ---
    repo = EmployeeRepositoryClass(session)
    emp_id = uuid4()

    employee = Employee(id=emp_id, employee_code='TEST-REPO', status=EmployeeStatus.ACTIVE)
    session.add(employee)

    p_info = EmployeePersonalInfo(
        employee_id=emp_id,
        first_name='Sensitive',
        last_name='Data',
        document_number='123456',
        personal_email='sensitive@test.com',
    )
    session.add(p_info)
    session.commit()

    p_info_id = p_info.id

    # --- ACT ---
    repo.soft_delete(employee)

    # --- ASSERT ---
    session.expire_all()

    repo.get_by_id(emp_id)

    raw_emp = session.get(Employee, emp_id)

    assert raw_emp is not None
    assert raw_emp.status == EmployeeStatus.TERMINATED
    assert raw_emp.deleted_at is not None

    deleted_info = session.get(EmployeePersonalInfo, p_info_id)
    assert deleted_info is None


def test_repo_get_by_id_excludes_deleted(session: Session) -> None:
    # --- ARRANGE ---
    repo = EmployeeRepositoryClass(session)
    emp_id = uuid4()

    deleted_emp = Employee(
        id=emp_id,
        employee_code='GHOST',
        status=EmployeeStatus.TERMINATED,
        deleted_at=datetime.now(),
    )
    session.add(deleted_emp)
    session.commit()

    # --- ACT ---
    result = repo.get_by_id(emp_id)

    # --- ASSERT ---
    assert result is None
