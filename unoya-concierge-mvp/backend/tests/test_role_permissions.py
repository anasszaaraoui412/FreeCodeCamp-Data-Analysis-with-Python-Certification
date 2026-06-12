import pytest
from app.models.models import User, UserRole
import uuid

def test_admin_can_list_users(client, db):
    # Create an admin user
    admin = User(
        id=uuid.uuid4(),
        email="admin@example.com",
        role=UserRole.tenant_admin,
        first_name="Admin"
    )
    db.add(admin)
    db.commit()

    headers = {"X-Mock-Role": "tenant_admin", "X-Mock-User-Email": "admin@example.com"}
    response = client.get("/api/v1/users", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_employee_cannot_list_users(client, db):
    # Create an employee user
    emp = User(
        id=uuid.uuid4(),
        email="emp@example.com",
        role=UserRole.employee,
        first_name="Emp"
    )
    db.add(emp)
    db.commit()

    headers = {"X-Mock-Role": "employee", "X-Mock-User-Email": "emp@example.com"}
    response = client.get("/api/v1/users", headers=headers)
    assert response.status_code == 403
