

```markdown
# 🗳️ Online Poll System  
**Real-time voting with secure authentication – built with FastAPI + Vanilla JS**

<img width="1786" height="934" alt="image" src="https://github.com/user-attachments/assets/90e24cf3-ab43-4d81-9e48-2644c67c3da9" />

---

## ✨ Features

- 🔐 **User Signup & Login** with JWT authentication
- 📝 **Create polls** with multiple options
- 🗳️ **Vote** on polls (one vote per user per poll)
- 👑 **Vote results visible only to poll creator** (authority mode)
- 📊 **Total votes count** shown to creator
- 🌐 **CORS enabled** – works perfectly with frontend
- ⚡ **Fast & lightweight** – FastAPI backend + pure HTML/CSS/JS frontend
- 🔄 **Auto-refresh** after voting

## 🚀 Tech Stack

| Layer       | Technology              | Purpose                              |
|-------------|--------------------------|--------------------------------------|
| Backend     | FastAPI                  | API, authentication, business logic  |
| Auth        | JWT + bcrypt             | Secure tokens & password hashing     |
| Frontend    | HTML + CSS + Vanilla JS  | Simple, no-framework UI              |
| Storage     | In-memory lists          | Quick prototyping (no database)      |
| CORS        | FastAPI middleware       | Allows frontend-backend communication|

## 📂 Project Structure

```
ONLINE_POLL_SYSTEM/
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Dependencies (fastapi, uvicorn, pydantic, bcrypt, pyjwt)
├── frontend/
│   ├── index.html           # Login & Signup page
│   └── polls.html           # Polls listing + create + vote page
├── .gitignore
└── README.md                ← You are here 😄
```

## 🛠️ Quick Start

### 1. Backend

```bash
# Go to backend folder
cd backend

# Install dependencies
pip install fastapi uvicorn pydantic bcrypt pyjwt

# Run the server
uvicorn main:app --reload --port 8000
```

API will be available at:  
→ http://127.0.0.1:8000  
→ Interactive docs: http://127.0.0.1:8000/docs

### 2. Frontend

```bash
# Go to frontend folder
cd frontend

# Start simple static server
python3 -m http.server 5500
# or: python -m http.server 5500  (Windows sometimes)
```

Open in browser:  
→ http://localhost:5500/index.html

### 3. How to use

1. Signup / Login  
2. Create a poll  
3. Share link or let others login & vote  
4. **Only you (creator)** can see the vote counts & total

## 🎯 Future Improvements Ideas

- [ ] Add real database (SQLite / PostgreSQL)
- [ ] Poll closing / expiration date
- [ ] Public results toggle by creator
- [ ] Bar chart / pie chart for results (Chart.js)
- [ ] Logout button
- [ ] User profile / my polls list
- [ ] Deploy to Render / Railway / Vercel

## ❤️ Made with

- ☕ Coffee  
- 💻 Late-night coding  
- 😄 Fun & learning

Feel free to fork, star ⭐ or contribute!

Happy polling! 🗳️✨
