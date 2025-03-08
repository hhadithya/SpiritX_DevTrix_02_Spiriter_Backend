from config.firebase_config import db
from typing import List, Optional

players_collection = db.collection("players")


# But maybe we might not use this instead will directly use onSnapshot in the frontend
def get_all_players(category: Optional[str] = None) -> List[dict]:
    """Retrieve all players, optionally filtering by category."""
    query = players_collection
    if category:
        query = query.where("category", "==", category)
        query = query.where("active", "==", True)
    
    players = query.stream()
    return [{**player.to_dict(), "id": player.id} for player in players]

def get_player(player_id: str) -> Optional[dict]:
    """Retrieve a single active player by ID."""
    player_doc = players_collection.document(player_id).get()
    if player_doc.exists and player_doc.to_dict().get("activeStatus", False):
        return {**player_doc.to_dict(), "id": player_doc.id}
    return {"message": None}

def add_player(name: str, category: str , basePrice: float) -> dict:
    """Add a new player and return the created player data."""
    player_data = {
        "name": name,
        "category": category,
        "basePrice": basePrice,
        "activeStatus": True  # if this is false then is it considered as deleted
    }
    new_player_ref = players_collection.add(player_data)
    return {"id": new_player_ref[1].id, **player_data}

def update_player(player_id: str, updated_data: dict) -> Optional[dict]:
    """Update an existing player and return updated data."""
    player_ref = players_collection.document(player_id)
    if player_ref.get().exists:
        player_ref.update(updated_data)
        return {**updated_data, "id": player_id}
    return None

def delete_player(player_id: str) -> bool:
    """Delete a player by ID and return True if successful."""
    # player_ref = players_collection.document(player_id)
    # if player_ref.get().exists:
    #     player_ref.delete()
    #     return True
    # return False

    # Instead of deleting the player, we will just mark it as inactive
    return update_player(player_id, {"active": False}) is not None

