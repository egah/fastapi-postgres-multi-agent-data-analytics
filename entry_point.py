import os
import typing
import warnings
from main.generate_response import generate_response
from fastapi import FastAPI, Path, Query, HTTPException, status, Body, Depends
from pydantic import BaseModel, Field
import dotenv

warnings.filterwarnings("ignore")
dotenv.load_dotenv("./.env")


# FastAPI core concept : 
# path operation
# Query Parameters
# Path Parameters
# Body Parameters (Request Body)
# Fields
# Depends
# Security
# Annotated Parameters
# BasModel from pydantic
# async function role
# Payload : is the data sent to the server. 
# the payload has Content type (application/json mean the server expect a json format)
#here the payload is a json string obtain with json.dumps
# input validation 
# error handling
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


def get_api_key_func(openai_api_key: typing.Union[str, None]) -> str:
    if openai_api_key is None:
        openai_api_key = os.environ.get("OPENAI_API_KEY")
    return openai_api_key


@app.get("/")
async def read_root():
    return {"message": "Hi, welcome to the API. Go to /docs to see the documentation."}


@app.post("/generate_data_from_natural_language_query/")
async def generate_response_from_prompt(
    prompt: Prompt,
    openai_api_key: str = Body(None)
) -> typing.Dict[str, typing.Any]:
    """
    This endpoint use the OpenAI ChatGPT completion endpoint 
    to transform natural language into a SQL query and return the query result.
    """
    openai_api_key = get_api_key_func(openai_api_key)
    response = generate_response(prompt.raw_prompt, prompt.postgres_url, openai_api_key)
    return {"response": response}