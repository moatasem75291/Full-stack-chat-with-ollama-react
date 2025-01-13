from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from OllamaChat import OllamaChat

import logging
import uvicorn


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="app.log",
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
chat_service = OllamaChat()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4096, description="User message")


@app.post("/chat")
async def chat(chat_request: ChatRequest):
    """
    Endpoint to interact with the chat service.
    :param chat_request: ChatRequest containing the user's message.
    :return: Assistant's response or an error message.
    """
    try:
        logger.info(f"Received chat request: {chat_request.message}")

        response = await chat_service.chat(chat_request.message)

        if response.error:
            logger.warning(f"Chat service returned an error: {response.error}")
            raise HTTPException(status_code=400, detail=response.error)

        elif response.stream:
            logger.info(f"Generated response: {response.stream}")
            return StreamingResponse(response.stream, media_type="text/plain")

    except Exception as e:
        logger.error(f"Unexpected error processing chat request: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process the request. Please try again later.",
        )


@app.get("/get_history")
async def get_chat_history():
    """
    Endpoint to retrieve chat history.
    :return: List of chat messages or an error message.
    """
    try:
        history = chat_service.get_chat_history()

        if history.error:
            logger.warning(f"Chat history retrieval error: {history.error}")
            raise HTTPException(status_code=400, detail=history.error)

        logger.info(f"Retrieved chat history: {len(history.response)} messages")
        return {"history": history.response}
    except Exception as e:
        logger.error(f"Unexpected error retrieving chat history: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve chat history. Please try again later.",
        )


@app.delete("/delete_history")
async def clear_chat_history():
    """
    Endpoint to clear chat history.
    :return: Success message or an error message.
    """
    try:
        response = chat_service.clear_history()

        if response.error:
            logger.warning(f"Chat history clearing error: {response.error}")
            raise HTTPException(status_code=400, detail=response.error)

        logger.info("Chat history cleared successfully")
        return {"message": response.response}
    except Exception as e:
        logger.error(f"Unexpected error clearing chat history: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to clear chat history. Please try again later.",
        )


@app.get("/")
async def health_check():
    """
    Health check endpoint.
    :return: Health status message.
    """
    try:
        return {"message": "OllamaChat service is running."}
    except Exception as e:
        logger.error(f"Unexpected error in health check: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to check service health. Please try again later.",
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
