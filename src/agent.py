from typing import List
from .conversation import Conversation
from .base import Tool
import json
from rich.console import Console

logger = Console()


class Agent(Tool):
    """
    Orchestrates conversation processing by delegating tasks to tools.

    Attributes:
        description (str): Overview of the Agent's role.
        max_turns (int): Maximum attempts before defaulting to the fallback tool.
        fallback_tool (Tool): Fallback tool if the Agent doesn't conclude earlier.
        available_tools (dict): Mapping of tool names to instances.
    """

    def __init__(
        self,
        name: str,
        description: str,
        fallback_tool: Tool,
        max_turns: int = 3,
        terminating: bool = False,
        tools: List[Tool] = [],
    ):
        """Initialize an Agent with its name, description, tools, and fallback behavior."""
        super().__init__(name=name, terminating=terminating)
        self.description = description
        self.max_turns = max_turns
        self.available_tools = {tool.name: tool for tool in tools}
        self.fallback_tool = fallback_tool

    def run(self, conversation: Conversation) -> str:
        """
        Execute up to `max_turns`, choosing a tool each turn. If a tool is terminating,
        return its response immediately; otherwise, record the result and continue.
        """
        for turn in range(self.max_turns):
            tool, function_args = self.get_next_action(conversation)
            logger.log(
                f"[bold cyan]Using the {tool.name} tool with arguments {function_args}[/bold cyan]"
            )
            response = tool.run(conversation, **function_args)
            if tool.terminating:
                return response

            conversation.add_message(
                "user",
                f"The {tool.name} tool has been used with args {function_args} and it responded with {response}",
            )
        return self.fallback_tool.run(conversation)

    def get_next_action(self, conversation: Conversation) -> Tool:
        """
        Derive the next tool call from the conversation's structured response.
        Returns a tuple of (Tool, dict) for the tool and its arguments.
        """
        response = conversation.get_response(
            tool_choice="required",
            tools=[tool.get_config() for tool in self.available_tools.values()],
        )
        tool_calls = response.choices[0].message.tool_calls
        function_name = tool_calls[0].function.name
        function_args = json.loads(tool_calls[0].function.arguments)
        return self.available_tools[function_name], function_args

    def get_config(self) -> dict:
        """
        Return a dictionary representing this Agent's function configuration.
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
            },
        }
