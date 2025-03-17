from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openapi
import re
from pydantic import BaseModel

app = FastAPI()

# Enable CORS (for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:3000"] for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Current database for users before integration with AWS
users = {
    "josh": {"username": "josh", "password": "josh123"},
    "sergio": {"username": "sergio", "password": "sergio123"},
    "ronnie": {"username": "ronnie", "password": "ronnie123"},
}

# Define a Pydantic model for validation
class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/email/score")  # Define the correct endpoint
def get_score(user_email, user_url):
    response = openapi.analyze_email(user_email, user_url)
    first_line = response.split("\n")[0]
    score_match = re.search(r'\d+', first_line)
    score = int(score_match.group()) if score_match else None
    return { "score": score }

@app.post("/login")
def login(user: LoginRequest):
    # Directly access attributes from the Pydantic model
    if user.username in users and users[user.username]["password"] == user.password:
        return {"message": "Login successful", "user": user.username}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")