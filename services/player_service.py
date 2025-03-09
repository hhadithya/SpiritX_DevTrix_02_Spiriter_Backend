from config.firebase_config import db
from typing import List, Optional
from google.cloud.firestore import DocumentSnapshot
from google.api_core.exceptions import GoogleAPICallError, NotFound
from fastapi import HTTPException

players_collection = db.collection("players")

def get_all_players(category: Optional[str] = None) -> List[dict]:
    """Retrieve all active players, optionally filtering by category."""
    try:
        query = players_collection.where("activeStatus", "==", True)
        if category:
            query = query.where("category", "==", category)

        players = query.stream()
        return [{**player.to_dict(), "id": player.id} for player in players]
    
    except GoogleAPICallError as e:
        raise HTTPException(status_code=503, detail="Database connection error. Please try again later.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error fetching players: {str(e)}")

def get_player(player_id: str) -> dict:
    """Retrieve a single active player by ID."""
    try:
        player_doc: DocumentSnapshot = players_collection.document(player_id).get()
        
        if not player_doc.exists:
            raise HTTPException(status_code=404, detail="Player not found")

        player_data = player_doc.to_dict()
        if not player_data.get("activeStatus", False):
            raise HTTPException(status_code=404, detail="Player is inactive")

        return {**player_data, "id": player_doc.id}

    except HTTPException as http_err:
        raise http_err  # Ensures proper HTTP response codes for known errors

    except GoogleAPICallError as api_err:
        raise HTTPException(status_code=503, detail="Database connection issue. Please try again later.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {str(e)}")

def add_player(name: str, category: str, basePrice: float) -> dict:
    """Add a new player."""
    try:
        player_data = {
            "name": name,
            "category": category,
            "basePrice": basePrice,
            "activeStatus": True
        }
        new_player_ref = players_collection.add(player_data)
        return {"id": new_player_ref[1].id, **player_data}
    
    except GoogleAPICallError:
        raise HTTPException(status_code=503, detail="Failed to connect to database. Please try again later.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error adding player: {str(e)}")

def update_player(player_id: str, updated_data: dict) -> dict:
    """Update a player."""
    try:
        player_ref = players_collection.document(player_id)
        player_doc = player_ref.get()
        if not player_doc.exists:
            raise HTTPException(status_code=404, detail="Player not found")
        
        player_ref.update(updated_data)
        return {**updated_data, "id": player_id}

    except NotFound:
        raise HTTPException(status_code=404, detail="Player not found")
    except GoogleAPICallError:
        raise HTTPException(status_code=503, detail="Database connection issue. Please try again later.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error updating player: {str(e)}")

def delete_player(player_id: str) -> bool:
    """Mark player as inactive instead of deleting."""
    try:
        return update_player(player_id, {"activeStatus": False})
    except HTTPException:
        raise  # Re-raise existing HTTP exceptions (e.g., if player is not found)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error deleting player: {str(e)}")
