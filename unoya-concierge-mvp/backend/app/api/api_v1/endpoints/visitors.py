from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.models import User, UserRole, Visitor, VisitorStatus
from app.schemas import schemas
from typing import List
from uuid import UUID
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[schemas.VisitorOut])
def list_visitors(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.role == UserRole.employee:
        return db.query(Visitor).filter(Visitor.host_id == current_user.id).all()
    return db.query(Visitor).all()

@router.post("/", response_model=schemas.VisitorOut)
def create_visitor(
    visitor_in: schemas.VisitorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    visitor = Visitor(**visitor_in.dict())
    db.add(visitor)
    db.commit()
    db.refresh(visitor)
    return visitor

@router.post("/{visitor_id}/check-in", response_model=schemas.VisitorOut)
def check_in_visitor(
    visitor_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.check_role([UserRole.receptionist, UserRole.tenant_admin]))
):
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    visitor.status = VisitorStatus.checked_in
    visitor.actual_arrival = datetime.utcnow()
    db.commit()
    db.refresh(visitor)
    return visitor
