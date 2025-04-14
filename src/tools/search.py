from ..base import Tool
from ..conversation import Conversation
from tavily import TavilyClient
import os


class Search(Tool):
    def __init__(self, terminating: bool = False):
        super().__init__(name="search", terminating=terminating)
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def run(self, conversation: Conversation, query: str) -> str:
        response = self.tavily_client.search(query)
        return response

    def get_config(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Execute a search query using Tavily Search",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query to search for",
                        },
                    },
                    "required": ["query"],
                },
            },
        }
