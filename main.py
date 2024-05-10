from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    password: str
    

app = FastAPI()


db = {}


@app.get('/')
def home():
    return "home" 


# @app.post("/signup", response_model=User)
# async def sign_up(user: User):
#     if user.username in _db:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
#     fake_db[user.username] = user
#     return  {'message': 'SignUp successfully', 'data': User}



@app.post("/signup")
async def sign_up(user: User):
    if user.username in db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    db[user.username] = user
    return {'message': 'Sign-up successful'}



@app.post("/signin")
async def sign_in(user: User):
    stored_user = db.get(user.username)
    if stored_user is None or stored_user.password != user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
     
    return {"message": "Signin successful"} 


@app.get("/users")
async def get_users():
    return list(db.values())


@app.get("/users/{username}")
async def get_single_user(username: str):
    if username not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return db[username]


@app.put("/users/{username}")
async def update_user(username: str, new_user: User):
    if username not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db[username] = new_user
    return {'message': 'User updated successfully'}


@app.delete("/users/{username}")
async def delete_user(username: str):
    if username not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    del db[username]
    return {'message': 'User deleted successfully'}