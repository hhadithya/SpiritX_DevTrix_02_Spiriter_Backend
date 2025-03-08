import pandas as pd
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

dataset_path = "data/sample_data.csv"
df = pd.read_csv(dataset_path)

df["search_text"] = df.apply(lambda x: (
    f"{x['Name']}, from {x['University']}, plays in {x['Category']}. "
    f"He has scored {x['Total Runs']} runs from {x['Balls Faced']} balls in {x['Innings Played']} innings. "
    f"He has taken {x['Wickets']} wickets, bowled {x['Overs Bowled']} overs, conceding {x['Runs Conceded']} runs."    
), axis=1)

vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(df["search_text"]).toarray()

dimension = vectors.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(vectors).astype(np.float32))

def search_player(query: str):
    query_vector = vectorizer.transform([query]).toarray().astype(np.float32)
    _, indices = index.search(query_vector, k=1)
    best_match = df.iloc[indices[0][0]]

    return best_match["Name"], best_match["search_text"]