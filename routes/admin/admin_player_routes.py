from fastapi import APIRouter, HTTPException, Query
from services.player_service import get_all_players, get_player, add_player, update_player, delete_player
from typing import List, Optional
from pydantic import BaseModel, Field

###### Player Management Routes ########
player_router = APIRouter(
    prefix="/players",
    tags=["players"],
)

class PlayerCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    category: str = Field(..., min_length=2, max_length=30)
    basePrice: float = Field(..., gt=0)  # Ensure base price is > 0

class PlayerUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    category: Optional[str] = Field(None, min_length=2, max_length=30)
    basePrice: Optional[float] = Field(None, gt=0)
    activeStatus: Optional[bool] = None

@player_router.get("/", response_model=List[dict])
def list_players(category: Optional[str] = Query(None, min_length=2, max_length=30)):
    return get_all_players(category)

@player_router.get("/{player_id}", response_model=dict)
def read_player(player_id: str):
    return get_player(player_id)

@player_router.post("/", response_model=dict)
def create_player(player: PlayerCreateRequest):
    return add_player(player.name, player.category, player.basePrice)

@player_router.put("/{player_id}", response_model=dict)
def update_existing_player(player_id: str, updated_player: PlayerUpdateRequest):
    updated_data = updated_player.model_dump(exclude_unset=True)
    if not updated_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    return update_player(player_id, updated_data)

@player_router.delete("/{player_id}")
def remove_player(player_id: str):
    return delete_player(player_id)
