from fastapi import FastAPI, HTTPException, Depends, Header, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import httpx
from dotenv import load_dotenv
import uuid

load_dotenv()

app = FastAPI(title="INCOGNITECH Backend")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Config
url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

# Headers needed for talking to Supabase REST and Auth API
supabase_headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

# --- Pydantic Models ---
class SignupModel(BaseModel):
    name: str
    email: str
    password: str

class LoginModel(BaseModel):
    email: str
    password: str

class EventRegistrationModel(BaseModel):
    name: str
    email: str
    college: str
    eventId: str

class PitchModel(BaseModel):
    name: str
    email: str
    message: str

# --- Authentication Helpers ---
async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    
    # Verify token with Supabase Auth API
    auth_url = f"{url}/auth/v1/user"
    async with httpx.AsyncClient() as client:
        res = await client.get(
            auth_url,
            headers={
                "apikey": key,
                "Authorization": f"Bearer {token}"
            }
        )
        if res.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        return res.json()

# --- Endpoints ---

@app.post("/api/auth/signup")
async def signup(user: SignupModel):
    signup_url = f"{url}/auth/v1/signup"
    payload = {
        "email": user.email,
        "password": user.password,
        "data": {
            "name": user.name
        }
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(signup_url, headers=supabase_headers, json=payload)
        data = res.json()
        if res.status_code >= 400:
            raise HTTPException(status_code=400, detail=data.get("msg", "Signup failed"))
            
        return {
            "token": data.get("access_token", "please-confirm-email"),
            "name": user.name,
            "email": user.email,
            "role": "student",
            "avatar": None
        }

@app.post("/api/auth/login")
async def login(user: LoginModel):
    login_url = f"{url}/auth/v1/token?grant_type=password"
    payload = {
        "email": user.email,
        "password": user.password
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(login_url, headers=supabase_headers, json=payload)
        data = res.json()
        if res.status_code >= 400:
            raise HTTPException(status_code=400, detail=data.get("error_description", "Invalid credentials"))
            
        user_meta = data.get("user", {}).get("user_metadata", {})
        return {
            "token": data.get("access_token"),
            "name": user_meta.get("name", ""),
            "email": user.email,
            "role": user_meta.get("role", "student"),
            "avatar": user_meta.get("avatar")
        }

@app.get("/api/blogs")
async def get_blogs():
    # Public endpoint to get blogs
    db_url = f"{url}/rest/v1/blogs?select=*"
    async with httpx.AsyncClient() as client:
        res = await client.get(db_url, headers=supabase_headers)
        data = res.json()
        if res.status_code >= 400:
            raise HTTPException(status_code=500, detail=f"Failed to fetch blogs: {data}")
        return {"count": len(data), "data": data}

@app.post("/api/blogs")
async def create_blog(
    title: str = Form(...),
    description: str = Form(...),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    authorization: str = Header(None)
):
    user = await get_current_user(authorization)
    user_id = user.get("id")
    user_meta = user.get("user_metadata", {})
    
    image_url = None
    if image:
        try:
            file_extension = image.filename.split(".")[-1]
            file_name = f"{uuid.uuid4()}.{file_extension}"
            
            # Upload to Supabase Storage using HTTP API
            storage_url = f"{url}/storage/v1/object/blogs/{file_name}"
            upload_headers = {
                "apikey": key,
                "Authorization": authorization,  # user token
                "Content-Type": image.content_type
            }
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    storage_url,
                    headers=upload_headers,
                    content=await image.read()
                )
                if res.status_code < 400:
                    image_url = f"{url}/storage/v1/object/public/blogs/{file_name}"
        except Exception as e:
            print("Error uploading image:", e)

    try:
        db_url = f"{url}/rest/v1/blogs"
        payload = {
            "title": title,
            "description": description,
            "content": content,
            "image": image_url,
            "author_id": user_id,
            "author": {
                "name": user_meta.get("name", "Unknown"),
                "avatar": user_meta.get("avatar")
            }
        }
        # Insert requires specific header
        insert_headers = supabase_headers.copy()
        insert_headers["Prefer"] = "return=representation"
        
        async with httpx.AsyncClient() as client:
            res = await client.post(db_url, headers=insert_headers, json=payload)
            if res.status_code >= 400:
                raise HTTPException(status_code=500, detail="Failed to create blog")
            return {"message": "Blog created successfully", "data": res.json()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/events")
async def get_events():
    db_url = f"{url}/rest/v1/events?select=*"
    async with httpx.AsyncClient() as client:
        res = await client.get(db_url, headers=supabase_headers)
        data = res.json()
        if res.status_code >= 400:
            raise HTTPException(status_code=500, detail=f"Failed to fetch events: {data}")
        return {"count": len(data), "data": data}

@app.post("/api/register-event")
async def register_event(registration: EventRegistrationModel, authorization: str = Header(None)):
    user = await get_current_user(authorization)
    user_id = user.get("id")
    
    try:
        db_url = f"{url}/rest/v1/event_registrations"
        payload = {
            "user_id": user_id,
            "name": registration.name,
            "email": registration.email,
            "college": registration.college,
            "event_id": registration.eventId
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(db_url, headers=supabase_headers, json=payload)
            if res.status_code >= 400:
                raise HTTPException(status_code=500, detail="Failed to register")
            return {"message": "Successfully registered for event"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact")
async def contact_pitch(pitch: PitchModel, authorization: str = Header(None)):
    if authorization:
        try:
            await get_current_user(authorization)
        except:
            pass # ignore auth error for pitch
            
    try:
        db_url = f"{url}/rest/v1/pitches"
        payload = {
            "name": pitch.name,
            "email": pitch.email,
            "message": pitch.message
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(db_url, headers=supabase_headers, json=payload)
            if res.status_code >= 400:
                raise HTTPException(status_code=500, detail="Failed to submit pitch")
            return {"message": "Pitch submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/profile")
async def update_profile(
    name: str = Form(...),
    avatar: Optional[UploadFile] = File(None),
    authorization: str = Header(None)
):
    user = await get_current_user(authorization)
    
    avatar_url = None
    if avatar:
        try:
            file_extension = avatar.filename.split(".")[-1]
            file_name = f"{uuid.uuid4()}.{file_extension}"
            
            # Upload to Supabase Storage using HTTP API
            storage_url = f"{url}/storage/v1/object/blogs/{file_name}"
            upload_headers = {
                "apikey": key,
                "Authorization": authorization,
                "Content-Type": avatar.content_type
            }
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    storage_url,
                    headers=upload_headers,
                    content=await avatar.read()
                )
                if res.status_code < 400:
                    avatar_url = f"{url}/storage/v1/object/public/blogs/{file_name}"
        except Exception as e:
            print("Error uploading avatar:", e)

    # Update user metadata in Supabase Auth
    user_metadata = user.get("user_metadata", {})
    user_metadata["name"] = name
    if avatar_url:
        user_metadata["avatar"] = avatar_url

    update_url = f"{url}/auth/v1/user"
    update_payload = {
        "data": user_metadata
    }
    async with httpx.AsyncClient() as client:
        res = await client.put(
            update_url,
            headers={
                "apikey": key,
                "Authorization": authorization,
                "Content-Type": "application/json"
            },
            json=update_payload
        )
        if res.status_code >= 400:
            raise HTTPException(status_code=500, detail="Failed to update profile")
        
        updated_data = res.json()
        updated_meta = updated_data.get("user_metadata", {})
        
        return {
            "name": updated_meta.get("name"),
            "avatar": updated_meta.get("avatar")
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
