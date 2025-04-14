from ..base import Tool
from ..conversation import Conversation
from tavily import TavilyClient
import os


class Extract(Tool):
    def __init__(self, terminating: bool = False):
        super().__init__(name="extract", terminating=terminating)
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def run(self, conversation: Conversation, urls: list[str]) -> str:
        response = self.tavily_client.extract(urls)
        return response

    def get_config(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Extract web page content from one or more specified URLs using Tavily Extract",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "urls": {
                            "type": "string",
                            "description": "The urls to extract from",
                        },
                    },
                    "required": ["urls"],
                },
            },
        }
