from abc import ABC, abstractmethod
from typing import Dict, Any

from .conversation import Conversation


class Tool(ABC):
    """
    An abstract base class representing a generic tool.

    Attributes:
        name (str): A unique name identifying the tool.
        terminating (bool): If True, using this tool should conclude the conversation
                            or process.
    """

    def __init__(self, name: str, terminating: bool = False):
        """Initialize a Tool with a name and an optional terminating flag."""
        self.name = name
        self.terminating = terminating

    @abstractmethod
    def run(self, conversation: Conversation) -> str:
        """
        Execute the tool's logic using the provided Conversation.

        Args:
            conversation (Conversation): The conversation context to operate on.

        Returns:
            str: The result or output of the tool's execution.
        """
        pass

    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """
        Provide a configuration dictionary describing the tool.

        Returns:
            dict: A dictionary containing metadata about the tool.
        """
        pass
