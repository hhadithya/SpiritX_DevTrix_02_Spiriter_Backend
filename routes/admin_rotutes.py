from fastapi import APIRouter
from services.player_service import get_all_players, get_player, add_player, update_player, delete_player
from typing import List, Optional

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


###### Player managment routes ########
player_router = APIRouter(
    prefix="/players",
    tags=["players"],
)

@player_router.get("/", response_model=List[dict])
def list_players(category: Optional[str] = None):
    return get_all_players(category)

@player_router.get("/{player_id}", response_model=dict)
def read_player(player_id: str):
    return get_player(player_id)

@player_router.post("/", response_model=dict)
def create_player(name: str, category: str , basePrice: float):
    return add_player(name, category, basePrice)

@player_router.put("/{player_id}", response_model=dict)
def update_existing_player(player_id: str, updated_player: dict):
    return update_player(player_id, updated_player)

@player_router.delete("/{player_id}")
def remove_player(player_id: str):
    return delete_player(player_id)

##################################
