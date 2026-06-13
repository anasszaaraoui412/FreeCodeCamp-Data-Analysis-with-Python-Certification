from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.models import User, UserRole, Message
from app.schemas import schemas
from typing import List
from uuid import UUID

router = APIRouter()

@router.get("/", response_model=List[schemas.MessageOut])
def list_messages(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.role == UserRole.employee:
        return db.query(Message).filter(Message.host_id == current_user.id).all()
    return db.query(Message).all()

@router.post("/", response_model=schemas.MessageOut)
def create_message(
    message_in: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    message = Message(**message_in.dict())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
