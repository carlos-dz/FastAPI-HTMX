from typing import Annotated

from fastapi import FastAPI, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


data_users = [
    {"name": "John Doe", "email": "john@example.com"},
    {"name": "Jane Doe", "email": "jane@example.com"},
    {"name": "Alice Smith", "email": "alice@example.com"},
    {"name": "Bob Willams", "email": "bob@example.com"},
    {"name": "Matty Laddy", "email": "matt@example.com"},
]


class User(BaseModel):
    name: str
    email: str


@app.get("/search", response_class=HTMLResponse)
async def root(q: Annotated[str, Query()]):
    results = [
        user
        for user in data_users
        if q.lower() in user["name"].lower() or q in user["email"]
    ]

    users_rows = [
        f"<tr><th>{user['name']}  -  </th><th>{user['email']}</th></tr>"
        for user in results
    ]

    return "".join(users_rows)


@app.post("/add-user", response_class=HTMLResponse)
async def add_user(name: Annotated[str, Form()], email: Annotated[str, Form()]):
    data_users.append({"name": name, "email": email})
    return f"{name} - {email} registered"


@app.post("/add-json-user", response_class=HTMLResponse)
async def add_json_user(user: User):
    data_users.append({"name": user.name, "email": user.email})
    return f"{user.name} - {user.email} registered"
