from fastapi import APIRouter
from app.api.api_v1.endpoints import users, bookings, rooms, visitors, messages

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
api_router.include_router(visitors.router, prefix="/visitors", tags=["visitors"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
