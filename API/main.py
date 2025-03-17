from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openapi
import re

app = FastAPI()

# Allow CORS for all domains (development only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; replace with ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/email/score")  # Define the correct endpoint
def get_score(user_email, user_url):
    response = openapi.analyze_email(user_email, user_url)
    first_line = response.split("\n")[0]
    score_match = re.search(r'\d+', first_line)
    score = int(score_match.group()) if score_match else None
    return { "score": score }