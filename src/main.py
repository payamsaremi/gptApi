import openai

import uvicorn

from fastapi import FastAPI, Request, Form
# from fastapi.responses import HTMLResponse

from pydantic import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = 'OPENAI_API_KEY'

    class Config:
        env_file = '.env'

settings = Settings()
openai.api_key = settings.OPENAI_API_KEY

app = FastAPI()


@app.get("/")
def index():
    return { "message": "hello world???"}


@app.post("/")
async def index(request: Request, animal: str= Form(...)):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(animal),
        temperature=0.6,
    )
    result = response.choices[0].text
    print("result", result)
    return {"result": result}


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.
Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)