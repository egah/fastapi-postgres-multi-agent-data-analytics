import os
from main.generate_response import generate_response
from fastapi import FastAPI, Path, Query, HTTPException, status, Body, Depends
from pydantic import BaseModel, Field
import dotenv

dotenv.load_dotenv("./.env")

"""
def main():
    parser = argparse.ArgumentParser("Generate a response from a prompt")
    parser.add_argument("--raw_prompt", help="The prompt for the AI")
    args = parser.parse_args()
    generate_response(args.raw_prompt)


if __name__ == "__main__":
    main()

"""


app = FastAPI()


class Prompt(BaseModel):
    raw_prompt: str = Field(
        ..., title="The prompt for the AI", description="The prompt for the AI"
    )
    postgres_url: str = Field(
        ...,
        title="The url for the postgres database",
        description="The url for the postgres database",
    )


def get_api_key_func():
    return os.environ.get("OPENAI_API_KEY")


@app.get("/")
async def read_root():
    return {"message": "Hi, welcome to the API. Go to /docs to see the documentation."}


@app.post("/generate_response/")
async def generate_response_from_prompt(
    prompt: Prompt, api_key: str = Depends(get_api_key_func)
):
    response = generate_response(prompt.raw_prompt, prompt.postgres_url)
    return {"response": response}