import pytest
from datetime import datetime, timedelta
from app.models.models import User, UserRole, Booking
import uuid

def test_booking_collision(client, db):
    # Create employee
    emp = User(
        id=uuid.uuid4(),
        email="booker@example.com",
        role=UserRole.employee,
        first_name="Booker"
    )
    db.add(emp)
    db.commit()

    start = datetime.utcnow() + timedelta(hours=1)
    end = start + timedelta(hours=1)

    # First booking
    headers = {"X-Mock-Role": "employee", "X-Mock-User-Email": "booker@example.com"}
    payload = {
        "host_id": str(emp.id),
        "start_time": start.isoformat(),
        "end_time": end.isoformat()
    }
    response = client.post("/api/v1/bookings/", json=payload, headers=headers)
    assert response.status_code == 200

    # Overlapping booking
    payload2 = {
        "host_id": str(emp.id),
        "start_time": (start + timedelta(minutes=30)).isoformat(),
        "end_time": (end + timedelta(minutes=30)).isoformat()
    }
    response = client.post("/api/v1/bookings/", json=payload2, headers=headers)
    assert response.status_code == 409
    assert "Schedule full" in response.json()["detail"]
