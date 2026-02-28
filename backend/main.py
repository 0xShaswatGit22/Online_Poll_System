from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import bcrypt
import jwt
import time

# Secret key for JWT (change this in production!)
SECRET_KEY = "supersecret"

app = FastAPI(title="Online Poll System")

# Allow frontend to call API (for local development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
users = []      # {name, email, password_hash}
polls = []      # {id, question, options, votes, voted_users, creator_email}

# ────────────────────────────────────────────────
# Pydantic Models
# ────────────────────────────────────────────────
class User(BaseModel):
    name: str | None = None
    email: str
    password: str

class PollCreate(BaseModel):
    question: str
    options: list[str]

class Vote(BaseModel):
    option_index: int

# ────────────────────────────────────────────────
# JWT Helpers
# ────────────────────────────────────────────────
def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing auth header")
    try:
        token = authorization.split(" ")[1]  # Bearer <token>
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = next((u for u in users if u["email"] == payload["email"]), None)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# ────────────────────────────────────────────────
# Auth Endpoints
# ────────────────────────────────────────────────
@app.post("/signup")
def signup(user: User):
    if any(u['email'] == user.email for u in users):
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    users.append({"name": user.name, "email": user.email, "password_hash": hashed})
    return {"status": "success", "message": "User created"}

@app.post("/login")
def login(user: User):
    u = next((u for u in users if u["email"] == user.email), None)
    if not u or not bcrypt.checkpw(user.password.encode(), u["password_hash"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = jwt.encode(
        {"email": u["email"], "exp": time.time() + 3600 * 24},  # 24 hours
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"status": "success", "token": token}

@app.get("/current-user")
def current_user(user=Depends(get_current_user)):
    return {"name": user["name"], "email": user["email"]}

# ────────────────────────────────────────────────
# Poll Endpoints
# ────────────────────────────────────────────────
@app.post("/polls")
def create_poll(poll: PollCreate, user=Depends(get_current_user)):
    poll_id = len(polls) + 1
    polls.append({
        "id": poll_id,
        "question": poll.question,
        "options": poll.options,
        "votes": [0] * len(poll.options),
        "voted_users": [],
        "creator_email": user["email"]           # ← key change
    })
    return {"status": "success", "poll_id": poll_id}

@app.get("/polls")
def get_polls():
    return polls

@app.get("/polls/{poll_id}")
def get_poll(poll_id: int):
    poll = next((p for p in polls if p["id"] == poll_id), None)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll

@app.post("/polls/{poll_id}/vote")
def vote(poll_id: int, vote: Vote, user=Depends(get_current_user)):
    poll = next((p for p in polls if p["id"] == poll_id), None)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    if user["email"] in poll["voted_users"]:
        raise HTTPException(status_code=400, detail="You have already voted")
    if vote.option_index < 0 or vote.option_index >= len(poll["options"]):
        raise HTTPException(status_code=400, detail="Invalid option index")
    poll["votes"][vote.option_index] += 1
    poll["voted_users"].append(user["email"])
    return {"status": "success"}

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Online Poll System API",
        "docs": "Visit /docs for interactive documentation",
        "endpoints": ["/signup", "/login", "/polls", "/polls/{poll_id}", "/polls/{poll_id}/vote"]
    }