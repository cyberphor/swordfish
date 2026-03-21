import asyncio
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Query
from fastapi.exceptions import RequestValidationError
from llama_cpp import Llama
from pydantic import BaseModel
from pydantic import field_validator


api = FastAPI()

model = Llama(
    model_path="smollm2-360m-instruct-q8_0.gguf",
    n_ctx=512,
    n_batch=1
)

MAX_TOKENS = 512

class ModelRequest(BaseModel):
    """
    A Model request.
    """
    message: str = Query("message")

    @field_validator("message")
    def check_message(cls, v) -> str:
        """
        Checks if the request exceeds the maximum token count.
        """
        tokens = len(model.tokenize(v.encode("utf-8")))
        if tokens >= MAX_TOKENS:
            raise RequestValidationError(f"Token count exceeds the maximum allowed limit of 512.")
        return v

@api.get("/healthcheck")
async def healthcheck():
    """
    Healthcheck.
    """
    return "OK"

@api.get("/api")
async def get_response(message: ModelRequest = Depends(ModelRequest)):
    """
    Gets a model response.
    """
    model_description = "You are an assistant."
    request = f"<|system|>\n{model_description}</s>\n<|user|>{message.message}</s><|assistant|>"
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None, lambda: model(request, temperature=0.0, max_tokens=MAX_TOKENS)
    )
    return response["choices"][0]["text"]
