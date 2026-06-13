from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User, UserRole
from app.core.config import settings

async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    if settings.MOCK_AUTH_ENABLED:
        role = request.headers.get("X-Mock-Role")
        email = request.headers.get("X-Mock-User-Email")

        if not role or not email:
            raise HTTPException(status_code=401, detail="Mock headers missing")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            # Auto-create user in mock mode for convenience to avoid deadlock
            user = User(
                email=email,
                first_name="Mock",
                last_name="User",
                role=UserRole(role) if role in [r.value for r in UserRole] else UserRole.employee,
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        return user

    # TODO: Implement Clerk Auth verification here
    raise HTTPException(status_code=501, detail="Clerk Auth not yet implemented")

def check_role(roles: list[UserRole]):
    async def role_checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker
