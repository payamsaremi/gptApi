import openai

import uvicorn

from fastapi import FastAPI, Request, Form, Depends, HTTPException, Header
# from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings, BaseModel

from fastapi.security.api_key import APIKey

from . import auth
from . import auth_handler

class Settings(BaseSettings):
    OPENAI_API_KEY: str = 'OPENAI_API_KEY'
    JWT_SECRET: str
    JWT_ALGORITHM: str

    class Config:
        env_file = '.env'

settings = Settings()
openai.api_key = settings.OPENAI_API_KEY

app = FastAPI()

origins = [
    "https://genoai.com",
    "https://genoai.com/dashboard",
    "https://apis.genoai.com",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return { "message": "Welcome to GenoAI's APIs"}

class Item(BaseModel):
    animal: str

@app.post("/")
async def index(item: Item, api_key: APIKey = Depends(auth.get_jwt)):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=item.animal,
        max_tokens=800,
        temperature=0.4,
    )
    result = response.choices[0].text
    print("result", result)
    return {"result": result}


@app.get('/secure')
async def secure(jwt: str = Depends(auth.get_jwt)):
    payload = auth_handler.validate_jwt(jwt, settings.JWT_SECRET, [settings.JWT_ALGORITHM])
    return {"message": "Welcome! You are authenticated. {}".format(payload)}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)