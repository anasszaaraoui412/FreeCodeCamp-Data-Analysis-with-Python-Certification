from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from app.models.models import UserRole, VisitorStatus, BookingStatus

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole
    department: Optional[str] = None
    office: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    department: Optional[str] = None
    office: Optional[str] = None
    is_active: Optional[bool] = None

class UserOut(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# Room Schemas
class RoomBase(BaseModel):
    name: str
    capacity: Optional[int] = None
    floor: Optional[str] = None
    equipment: Optional[List[str]] = None
    is_active: bool = True

class RoomCreate(RoomBase):
    pass

class RoomOut(RoomBase):
    id: UUID

    class Config:
        from_attributes = True

# Booking Schemas
class BookingBase(BaseModel):
    host_id: UUID
    room_id: Optional[UUID] = None
    start_time: datetime
    end_time: datetime
    status: BookingStatus = BookingStatus.confirmed

class BookingCreate(BookingBase):
    pass

class BookingOut(BookingBase):
    id: UUID

    class Config:
        from_attributes = True

# Visitor Schemas
class VisitorBase(BaseModel):
    full_name: str
    company: Optional[str] = None
    status: VisitorStatus = VisitorStatus.expected
    host_id: UUID
    expected_arrival: Optional[datetime] = None

class VisitorCreate(VisitorBase):
    pass

class VisitorOut(VisitorBase):
    id: UUID
    actual_arrival: Optional[datetime] = None

    class Config:
        from_attributes = True

# Message Schemas
class MessageBase(BaseModel):
    visitor_id: Optional[UUID] = None
    host_id: UUID
    content: str

class MessageCreate(MessageBase):
    pass

class MessageOut(MessageBase):
    id: UUID
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
