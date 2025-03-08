from fastapi import FastAPI
import pandas as pd

app = FastAPI()

dataset_path  = "sample_data.csv"
df = pd.read_csv(dataset_path)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/player/{player_name}")
def get_details(player_name: str):
    data = df[df["Name"].str.lower() == player_name.lower()]
    if data.empty:
         return {"response": "I don't have enough knowledge to answer that question."}
    return data.to_dict(orient="records")[0]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)