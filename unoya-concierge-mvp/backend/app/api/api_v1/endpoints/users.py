from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.models import User, UserRole, Room, Booking, Visitor, Message
from app.schemas import schemas
from typing import List
from uuid import UUID

router = APIRouter()

@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: User = Depends(deps.get_current_user)):
    return current_user

@router.get("/", response_model=List[schemas.UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.check_role([UserRole.tenant_admin]))
):
    return db.query(User).all()

@router.post("/", response_model=schemas.UserOut)
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.check_role([UserRole.tenant_admin]))
):
    user = User(**user_in.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
