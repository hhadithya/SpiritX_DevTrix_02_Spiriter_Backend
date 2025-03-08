from fastapi import FastAPI, Query
from retrieval import search_player
from generation import generate_response

app = FastAPI()

user_session = {}

@app.get("/")
def read_root():
    return {"message": "RAG Chatbot with Gemini is Running!"}

@app.get("/query/")
def query_chatbot(user_id: str, query: str = Query(..., description="Enter player-related query")):
    try:
        if user_id not in user_session:
            user_session[user_id] = []
        
        user_session[user_id].append(query)

        player_info = search_player(query)
        response = generate_response(query, player_info)

        return {"response": response}
    
    except Exception as e:
        print(query)
        return {"response": "I don't have enough knowledge to answer that question."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)