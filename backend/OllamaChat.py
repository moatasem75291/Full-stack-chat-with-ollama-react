import logging
from pydantic import BaseModel, Field
from typing import Optional, AsyncGenerator, List, Union

from llama_index.llms.ollama import Ollama
from llama_index.core import PromptTemplate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="ollama_chat.log",
)
logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    role: str = Field(default="user")
    content: str


class ChatResponse(BaseModel):
    response: Optional[Union[str, List[ChatMessage]]] = None
    metadata: dict = Field(default_factory=dict)
    error: Optional[str] = None
    stream: Optional[AsyncGenerator[str, None]] = None

    class Config:
        arbitrary_types_allowed = True


class OllamaChat:
    def __init__(self):
        self.system_prompt = """You are a helpful, respectful and honest assistant. 
        Always provide accurate information and if you're not sure about something, 
        admit it. Follow these rules:
        1. Keep responses clear and concise
        2. Use markdown formatting when appropriate
        3. If asked about coding, provide working examples
        4. Never generate harmful or unethical content
        5. Always maintain a professional tone
        """

        try:
            self.llm = Ollama(
                model="llama3.2:1b",
                temperature=0.7,
                context_window=4096,
                request_timeout=120.0,
            )
            logger.info("Ollama LLM initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Ollama LLM: {str(e)}")
            self.llm = None

        self.chat_history: List[ChatMessage] = []

    def _create_prompt(self, user_message: str) -> str:
        prompt_template = PromptTemplate(
            template=(
                "System: {system_prompt}\n"
                "Chat History: {chat_history}\n"
                "User: {user_message}\n"
                "Assistant: "
            )
        )

        chat_history_str = "\n".join(
            [f"{msg.role}: {msg.content}" for msg in self.chat_history[-5:]]
        )

        return prompt_template.format(
            system_prompt=self.system_prompt,
            chat_history=chat_history_str,
            user_message=user_message,
        )

    async def chat(self, message: str) -> ChatResponse:
        """
        Process user input and return a streaming response from the assistant.
        """
        if not self.llm:
            logger.error("LLM is not initialized")
            return ChatResponse(
                error="The assistant is currently unavailable. Please try again later."
            )

        try:
            logger.info(f"Received user message: {message}")
            prompt = self._create_prompt(message)

            async def response_generator():
                full_response = ""
                for chunk in self.llm.stream_complete(prompt):
                    if chunk.delta:
                        full_response += chunk.delta
                        yield chunk.delta

                self.chat_history.append(ChatMessage(role="user", content=message))
                self.chat_history.append(
                    ChatMessage(role="assistant", content=full_response)
                )

            logger.info("Initialized streaming response")
            return ChatResponse(stream=response_generator())

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return ChatResponse(error=f"[ERROR]: {str(e)}")

    def clear_history(self) -> ChatResponse:
        """
        Clear the chat history.
        """
        try:
            self.chat_history = []
            logger.info("Chat history cleared successfully")
            return ChatResponse(response="Chat history cleared.")
        except Exception as e:
            logger.error(f"Error clearing chat history: {str(e)}")
            return ChatResponse(error=f"[ERROR]: {str(e)}")

    def get_chat_history(self) -> ChatResponse:
        """
        Retrieve the chat history as a list of messages.
        """
        try:
            if not self.chat_history:
                return ChatResponse(response=[], metadata={})
            chat_history_list = [
                {"role": msg.role, "content": msg.content} for msg in self.chat_history
            ]
            return ChatResponse(response=chat_history_list, metadata={})
        except Exception as e:
            logger.error(f"Error retrieving chat history: {str(e)}")
            return ChatResponse(error=f"[ERROR]: {str(e)}")
