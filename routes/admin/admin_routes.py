from fastapi import APIRouter
from routes.admin.admin_player_routes import player_router

admin_router = APIRouter()

admin_router.include_router(player_router, prefix="/admin")

