from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.models import User, UserRole, Room
from app.schemas import schemas
from typing import List
from uuid import UUID

router = APIRouter()

@router.get("/", response_model=List[schemas.RoomOut])
def list_rooms(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return db.query(Room).all()

@router.post("/", response_model=schemas.RoomOut)
def create_room(
    room_in: schemas.RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.check_role([UserRole.tenant_admin]))
):
    room = Room(**room_in.dict())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room
