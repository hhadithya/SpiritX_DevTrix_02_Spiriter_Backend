from fastapi import FastAPI
import pandas as pd
from gemini_response import gemini_response

app = FastAPI()

dataset_path  = "sample_data.csv"
df = pd.read_csv(dataset_path)

@app.get("/")
def read_root():
    return {"message": "RAG Chatbot with Gemini is Running!"}

@app.get("/player/{player_name}")
def get_details(player_name: str):
    data = df[df["Name"].str.lower() == player_name.lower()]
    if data.empty:
         return {"response": "I don't have enough knowledge to answer that question."}
    
    response = gemini_response(player_name, data.to_string(index=False))

    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
