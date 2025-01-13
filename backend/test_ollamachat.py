import pytest
from unittest.mock import AsyncMock, patch
from OllamaChat import OllamaChat, ChatResponse


class TestOllamaChat:
    def setup_method(self):
        self.chat = OllamaChat()
        self.mock_response = AsyncMock()
        self.mock_response.text = "Test response"
        self.mock_response.additional_kwargs = {"timestamp": "2024-01-01"}

    @pytest.mark.asyncio
    async def test_send_message(self):
        with patch.object(self.chat.llm, "acomplete", return_value=self.mock_response):
            response = await self.chat.chat("Hello")
            assert isinstance(response, ChatResponse)
            assert response.response == "Test response"

    @pytest.mark.asyncio
    async def test_history_tracking(self):
        with patch.object(self.chat.llm, "acomplete", return_value=self.mock_response):
            await self.chat.chat("Hello")
            history = self.chat.get_chat_history()
            assert len(history) == 2
            assert history[0].content == "Hello"
            assert history[1].content == "Test response"

    def test_clear_history(self):
        self.chat.clear_history()
        assert len(self.chat.get_chat_history()) == 0

    @pytest.mark.asyncio
    async def test_empty_message(self):
        with pytest.raises(ValueError):
            await self.chat.chat("")

    @pytest.mark.asyncio
    async def test_api_error(self):
        with patch.object(
            self.chat.llm, "acomplete", side_effect=Exception("API Error")
        ):
            with pytest.raises(Exception) as exc:
                await self.chat.chat("Hello")
            assert "API Error" in str(exc.value)


import asyncio
from OllamaChat import OllamaChat


async def main():

    chat = OllamaChat()

    print("Welcome to OllamaChat!")
    print("Type your message or 'exit' to quit.")
    print("Commands:")
    print("  /history - View chat history")
    print("  /clear   - Clear chat history\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        elif user_input.lower() == "/history":
            history = chat.get_chat_history()
            if not history:
                print("No chat history available.")
            else:
                print("\nChat History:")
                for msg in history:
                    print(f"[{msg.role.capitalize()}] {msg.content}")
            print()
            continue
        elif user_input.lower() == "/clear":
            chat.clear_history()
            print("Chat history cleared.\n")
            continue

        try:
            response = await chat.chat(user_input)
            print(f"Ollama: {response.response}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
