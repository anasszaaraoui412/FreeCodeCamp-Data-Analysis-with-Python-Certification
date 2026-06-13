from fastapi import APIRouter, Depends, HTTPException
from livekit import api
from app.api import deps
from app.models.models import User
from app.core.config import settings

router = APIRouter()

@router.get("/livekit-token")
async def get_livekit_token(
    room: str = "concierge-room",
    current_user: User = Depends(deps.get_current_user)
):
    try:
        token = api.AccessToken(
            settings.LIVEKIT_API_KEY,
            settings.LIVEKIT_API_SECRET
        ) \
            .with_identity(f"user-{current_user.id}") \
            .with_name(f"{current_user.first_name} {current_user.last_name}") \
            .with_grants(api.VideoGrants(
                room_join=True,
                room=room,
            ))

        return {"token": token.to_jwt()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
