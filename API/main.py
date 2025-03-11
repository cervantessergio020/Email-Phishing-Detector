from fastapi import FastAPI
import random  # Import random for score generation

app = FastAPI()

@app.get("/email/score")  # Define the correct endpoint
def get_score():
    new_score = random.randint(0, 100)
    return {"score": new_score}

