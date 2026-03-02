import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def predict_batch(df: pd.DataFrame):

    payload = {
        "packets": df.to_dict(orient="records")
    }

    response = requests.post(
        f"{API_URL}/predict/batch",
        json=payload
    )

    return response.json()