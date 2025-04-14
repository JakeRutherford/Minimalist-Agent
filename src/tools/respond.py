from ..base import Tool
from ..conversation import Conversation
from typing import List
import jinja2


class Respond(Tool):
    def __init__(self, response_types: List[str], terminating: bool = True):
        # Mark this tool as terminating since its response is meant to be final.
        super().__init__(name="respond", terminating=terminating)
        self.response_types = response_types

    def run(self, conversation: Conversation, response_type: str = "") -> str:
        if not response_type:
            response_type = "respond"

        with open(f"templates/{response_type}.jinja2", "r") as file:
            template_content = jinja2.Template(file.read()).render()
        conversation.add_message("system", template_content)
        response = conversation.get_response(tool_choice=None)
        conversation.messages.pop()
        return response.choices[0].message.content

    def get_config(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "This tool provides responses for the given user message.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "response_type": {
                            "type": "string",
                            "description": "The type of response to be generated.",
                            "enum": self.response_types,
                        },
                    },
                    "required": ["response_type"],
                },
            },
        }
