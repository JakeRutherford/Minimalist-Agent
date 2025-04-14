import json
from copy import deepcopy
from typing import List

import jinja2
from pydantic import BaseModel
from rich.console import Console

from ..base import Tool
from ..conversation import Conversation

logger = Console()


class Section(BaseModel):
    """Represents a single report section with a title and description."""

    title: str
    description: str


class Outline(BaseModel):
    """Defines the overall report outline, including a title and multiple sections."""

    title: str
    sections: List[Section]


class Report(Tool):
    """
    A tool for generating a report. It creates an outline, then writes the report
    section by section using user-provided Jinja2 templates.
    """

    def __init__(self, terminating: bool = True):
        """
        Initialize the Report tool.

        Args:
            terminating (bool, optional): Indicates if using this tool should
                finalize or "terminate" the conversation. Defaults to True.
        """
        super().__init__(name="report", terminating=terminating)

    def run(self, conversation: Conversation) -> str:
        """
        Entrypoint for the Report tool. Generates an outline and writes the report.

        Args:
            conversation (Conversation): The conversation context (messages, model, etc.).

        Returns:
            str: The final report text.
        """
        outline = self.generate_outline(conversation)
        return self.write_report(conversation, outline)

    def write_report(self, conversation: Conversation, outline: Outline) -> str:
        """
        Write the report based on the provided outline. For each section:
         1. Uses a Jinja2 template to craft a prompt.
         2. Gets a response from the conversation.
         3. Appends the response to the growing report.

        Args:
            conversation (Conversation): The conversation context.
            outline (Outline): The structured outline guiding report creation.

        Returns:
            str: The completed report text.
        """
        report_conversation = deepcopy(conversation)
        report_so_far = f"# {outline.title}\n\n"

        for section in outline.sections:
            logger.log(f"[bold green]Writing section: {section.title}[/bold green]")
            with open("templates/write_report.jinja2", "r") as file:
                template_str = file.read()
            template = jinja2.Template(template_str).render(
                {
                    "outline": outline,
                    "current_section": section,
                    "report_so_far": report_so_far,
                }
            )

            report_conversation.add_message("user", template)
            response = report_conversation.get_response(tool_choice=None)
            report_so_far += response.choices[0].message.content + "\n\n"

        return report_so_far

    def generate_outline(self, conversation: Conversation) -> Outline:
        """
        Proposes a report outline by prompting the conversation with a template.

        Args:
            conversation (Conversation): The conversation context.

        Returns:
            Outline: The parsed outline model for the report.
        """
        logger.log("[bold green]Planning a structure for the report.[/bold green]")
        with open("templates/report_outline.jinja2", "r") as file:
            template_str = file.read()
        template = jinja2.Template(template_str).render()

        conversation.add_message("user", template)
        response = conversation.get_response(tool_choice=None, response_format=Outline)
        conversation.messages.pop()  # Remove the user prompt to keep conversation clean

        # Parse the model content from the LLM's JSON response
        return Outline(**json.loads(response.choices[0].message.content))

    def get_config(self) -> dict:
        """
        Return metadata describing this tool for higher-level orchestration systems.

        Returns:
            dict: A dictionary with the tool's function definition.
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Generate a comprehensive report based on the research.",
            },
        }
