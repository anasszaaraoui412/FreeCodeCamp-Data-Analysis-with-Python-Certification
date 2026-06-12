from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.api import deps
from app.core.database import get_db
from app.models.models import User, UserRole, Booking, BookingStatus
from app.schemas import schemas
from typing import List
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=schemas.BookingOut)
def create_booking(
    booking_in: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Collision Logic
    # Check if host is busy
    collision = db.query(Booking).filter(
        Booking.host_id == booking_in.host_id,
        Booking.status == BookingStatus.confirmed,
        or_(
            and_(Booking.start_time <= booking_in.start_time, Booking.end_time > booking_in.start_time),
            and_(Booking.start_time < booking_in.end_time, Booking.end_time >= booking_in.end_time),
            and_(Booking.start_time >= booking_in.start_time, Booking.end_time <= booking_in.end_time)
        )
    ).first()

    if collision:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Schedule full: Please select a different time."
        )

    # Check if room is busy (if room_id is provided)
    if booking_in.room_id:
        room_collision = db.query(Booking).filter(
            Booking.room_id == booking_in.room_id,
            Booking.status == BookingStatus.confirmed,
            or_(
                and_(Booking.start_time <= booking_in.start_time, Booking.end_time > booking_in.start_time),
                and_(Booking.start_time < booking_in.end_time, Booking.end_time >= booking_in.end_time),
                and_(Booking.start_time >= booking_in.start_time, Booking.end_time <= booking_in.end_time)
            )
        ).first()
        if room_collision:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room already booked for this time."
            )

    booking = Booking(**booking_in.dict())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@router.get("/", response_model=List[schemas.BookingOut])
def list_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.role == UserRole.employee:
        return db.query(Booking).filter(Booking.host_id == current_user.id).all()
    return db.query(Booking).all()
