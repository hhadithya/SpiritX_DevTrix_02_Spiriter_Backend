from fastapi import FastAPI, Query
from retrieval import search_player
from generation import generate_response

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "RAG Chatbot with Gemini is Running!"}

@app.get("/query/")
def query_chatbot(query: str = Query(..., description="Enter player-related query")):
    try:
        player_name, player_info = search_player(query)
        response = generate_response(player_name, player_info)
        return {"response": response}
    except Exception:
        return {"response": "I don't have enough knowledge to answer that question."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)