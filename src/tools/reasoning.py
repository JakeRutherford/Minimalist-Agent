from ..base import Tool
from ..conversation import Conversation
from typing import Dict, Any
import jinja2


class Reasoning(Tool):
    def __init__(self, terminating: bool = False):
        super().__init__(name="reasoning", terminating=terminating)

    def run(self, conversation: Conversation) -> str:
        with open("templates/reasoning.jinja2", "r") as file:
            reasoning_template = jinja2.Template(file.read()).render()
        conversation.add_message("system", reasoning_template)
        response = conversation.get_response(tool_choice=None)
        conversation.messages.pop()  # remove the reasoning message
        return response.choices[0].message.content

    def get_config(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "This tool provides reasoning for the given context.",
            },
        }
