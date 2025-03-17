from fastapi import FastAPI
import openapi
import re

app = FastAPI()

@app.get("/email/score")  # Define the correct endpoint
def get_score(user_email, user_url):
    response = openapi.analyze_email(user_email, user_url)
    first_line = response.split("\n")[0]
    score_match = re.search(r'\d+', first_line)
    score = int(score_match.group()) if score_match else None
    return { "score": score }