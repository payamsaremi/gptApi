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

@app.get('/secure')
async def secure(jwt: str = Depends(auth.get_jwt)):
    payload = auth_handler.validate_jwt(jwt, settings.JWT_SECRET, [settings.JWT_ALGORITHM])
    return {"message": "Welcome! You are authenticated. {}".format(payload)}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)



@app.get("/")
def index():
    return { "message": "Welcome to GenoAI's APIs"}

class Item(BaseModel):
    animal: str

@app.post("/old")
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



MODEL = "gpt-3.5-turbo"
system_prompt="""
The user will provide a description of what they wan to learn and you will create a slide deck based that.
Each slide must be entertaining, educational and captivate to the listener.
You must only write the JSON format of the slide deck as a runnable code. 
(Important: do not use double quotes inside the texts)
Example of what you should response with:
{
    "title": "an interesting title based on context of the presentation",
    "slides": [
        {
            "title": "Give a title to this slide",
            "content": "content of the presentation",
            "imagePrompt": "use the content of this slide to write a prompt for the AI to generate a realistic image, be contextual and based on facts"
        }
        continue for maximum 3 short slides
    ]
  },
"""
@app.post("/story-generator")
async def index(item: Item, api_key: APIKey = Depends(auth.get_jwt)):
    user_input=item.animal,
    response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a teacher narrating a presentation. only write in JSON format."},
        {"role": "system", "content": f'{system_prompt}'},
        {"role": "user", "content": f'{user_input}'},
        ],
    temperature=0,
)
    result = response['choices'][0]['message']['content']
    print("response", response)
    return {"result": result}




