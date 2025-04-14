from typing import List, Optional
from pydantic import BaseModel
from litellm import completion


class Conversation:
    """
    Manages a conversation by storing messages and retrieving responses
    from a specified language model.

    Attributes:
        model (str): The name of the language model to use for completion.
        messages (list): A list of dictionaries representing the conversation
                         history (role and content).
    """

    def __init__(self, model: str = "gpt-4.1-2025-04-14"):
        """
        Initialize a Conversation instance.

        Args:
            model (str, optional): The identifier for the language model.
                                   Defaults to "gpt-4.1-2025-04-14".
        """
        self.model = model
        self.messages = []

    def add_message(self, role: str, content: str) -> None:
        """
        Append a new message to the conversation history.

        Args:
            role (str): The role of the message (e.g., "user", "assistant", "system").
            content (str): The text content of the message.
        """
        self.messages.append({"role": role, "content": content})

    def get_response(
        self,
        tool_choice: str = "auto",
        tools: Optional[List] = None,
        response_format: BaseModel = None,
    ):
        """
        Request a completion (or response) from the language model via `litellm`.

        Args:
            tool_choice (str, optional): How tool usage should be handled by `litellm`.
                                         Defaults to "auto".
            tools (List, optional): A list of tool configurations. If None, `tool_choice`
                                    is disabled.
            response_format (BaseModel, optional): A Pydantic model defining the
                                                   expected structure of the response.

        Returns:
            Any: The structured response returned by `litellm.completion()`.
        """
        if tools is None:
            tool_choice = None

        return completion(
            model=self.model,
            messages=self.messages,
            tools=tools,
            tool_choice=tool_choice,
            response_format=response_format,
        )
