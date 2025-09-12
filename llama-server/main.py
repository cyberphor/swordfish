"""
A module for an Large Language Model (LLM).
"""

# import built-in modules
from typing import Any, Iterator, List, Optional, Union

# import third-party modules
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from llama_cpp import Llama, CreateCompletionResponse
from pydantic import BaseModel, validator

app = FastAPI()

# declare and initialize a variable called "model" by assigning a Llama object to it
model = Llama(model_path="gemma-3-1b-pt-q4_0.gguf")

# set the max number of tokens allowed for each LLM prompt
MAX_TOKENS = 512

# create a class called "LLMRequest" to represent each request sent to the LLM
class LLMRequest(BaseModel):
    """
    Represents requests sent to the Large Language Model (LLM)
    """

    # declare a property called "message" for the "LLMRequest" class and initialize it using a Query object
    # the "message" property will be whatever is passed via the "message" field
    message: str = Query("message")

    # the "cls" parameter is the "LLMRequest" class
    # the "v" parameter is the "message" property
    @validator("message")
    def check_message(cls: Any, v: str) -> str:
        """
        Checks if the request exceeds the maximum token count
        """
        # if the number of "tokens" used exceeds what is allowed, throw an error
        tokens = len(model.tokenize(v.encode("utf-8")))
        if tokens >= MAX_TOKENS:
            raise RequestValidationError(
                "Token count exceeds the maximum allowed limit of 512."
            )
        # otherwise return what was passed via the "message" field
        return v


# create a class called "LLMChoices" to describe LLM choices
class LLMChoices(BaseModel):
    """
    Represents Large Language Model (LLM) choices
    """

    text: str = "Beep boop"
    index: int = 0
    logprobs: Optional[str] = "null"
    finish_reason: str = "stop"


# create a class called "LLMUsage" to describe LLM token usage
class LLMUsage(BaseModel):
    """
    Represents Large Language Model (LLM) token usage
    """

    prompt_tokens: int = 198
    completion_tokens: int = 10
    total_tokens: int = 208


# create a class called "BaseLlamaResponse" to represent each response from the LLM
class BaseLlamaResponse(BaseModel):
    """
    Represents responses from the Large Language Model (LLM)
    """

    id: str = "cmpl-7fc1be4c-8f5b-4b2f-805f-f8c5086a9fb4"
    object: str = "text_completion"
    created: int = 1708459650
    #model: str = "tinyllama-1.1b-chat-v1.0.Q2_K.gguf"
    model: str = "gemma-3-1b-pt-q4_0.gguf"
    choices: List[LLMChoices]
    usage: LLMUsage = LLMUsage()


# add a HTTP route, with an endpoint called "/healthcheck", to the FastAPI app
@app.get("/healthcheck")
async def healthcheck() -> str:
    """
    Function to check if the FastAPI app is running
    """
    return "OK"


# add a HTTP route, with an endpoint called "/api", to the FastAPI FastAPI app
@app.post("/api", response_model=BaseLlamaResponse)
async def api(
    message,
) -> Union[CreateCompletionResponse, Iterator[CreateCompletionResponse]]:
    """
    Function to implement the Large Language Model's (LLM) Application Programming Interface (API)
    """
    #model_description = "You are a cybersecurity assistant."
    #request = f"<|system|>\n{model_description}</s>\n<|user|>{message}</s><|assistant|>"
    #response = model(request, temperature=0.2, max_tokens=MAX_TOKENS)
    response = model(
	    message,
	    max_tokens=512,
	    echo=True,
    )
    return response
