import openai

import uvicorn

from fastapi import FastAPI, Request, Form
# from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings, BaseModel



class Settings(BaseSettings):
    OPENAI_API_KEY: str = 'OPENAI_API_KEY'

    class Config:
        env_file = '.env'

settings = Settings()
openai.api_key = settings.OPENAI_API_KEY

app = FastAPI()

origins = [
    "http://localhost",
    "https://genoai.com/",
    "https://genoai.com/dashboard",
     "http://localhost:3000",
     "http://127.0.0.1:3000",
    "http://localhost:3001",
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
    return { "message": "hello world???"}

class Item(BaseModel):
    animal: str

@app.post("/")
async def index(item: Item):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=item.animal,
        max_tokens=800,
        temperature=0.4,
    )
    result = response.choices[0].text
    print("result", result)
    return {"result": result}


# myDict = {
#       "id": "st-1",
#       "title": "place a title based on the context of story here",
#       "slides": [
#           {
#               "title": "Give a title to this slide",
#               "content": "This is the first slide of Story 1",
#               "imagePrompt": "use your imagination to write a prompt for the AI to generate an image based on the content of this slide, be highly detaile and also abstract but contextual"
#           },
#           {
#               "title": "Give a title to this slide",
#               "content": "This is the second slide of Story 1",
#               "imagePrompt": "use your imagination to write a prompt for the AI to generate an image based on the content of this slide, be highly detaile and also abstract but contextual"
#           },
#           {
#               "title": "Give a title to this slide",
#               "content": "This is the third slide of Story 1",
#               "imagePrompt": "use your imagination to write a prompt for the AI to generate an image based on the content of this slide, be highly detaile and also abstract but contextual"
#           }
#       ]
#     },

# def generate_prompt(animal):
#     if animal is None:
#         return "Error: animal is undefined"

#     return '''
#     Input: {}
#     ----------------------------
#     Write a detailed story for the product, idea or write a novel.
#     detect the language of user and translate your story to that language.
#     here is just an example of how the JSON output should look like. (Important: do not use double quites inside the texts):

#     {}

#     -----------------------------
#     Here are the results:
#     '''.format(
#         animal.capitalize(),
#         myDict
#     )

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)