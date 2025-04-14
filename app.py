"""
app.py

This script implements a CLI Chat Application that utilizes two agents:
1. A main agent (`main_agent`) designed to interact with the user and
   handle general conversation.
2. A research agent (`research_agent`) designed to autonomously carry
   out market research tasks.

The agents work together with a set of tools to provide a conversational
interface for market research.

Usage:
    python app.py [--main_turns N] [--research_turns N]

    - Type your message and press Enter to interact with the main agent.
    - Use the 'reset' command to reset the conversation (retaining the system prompt).
    - Use the 'exit' or 'quit' command to exit the chat.

Command-line Arguments:
    --main_turns       Maximum number of turns the main agent can take in a single run.
    --research_turns   Maximum number of turns the research agent can take in a single run.
"""

import argparse
from datetime import datetime
import jinja2
import sys
from dotenv import load_dotenv

from rich.console import Console
from rich.prompt import Prompt
from rich.markdown import Markdown

from src.conversation import Conversation
from src.agent import Agent
from src.tools import Respond, Search, Extract, Reasoning, Report

load_dotenv()


def main():
    """
    The main entry point for the CLI Chat Application.

    Raises:
        SystemExit: If the system message template cannot be read or other
                    system-level errors occur.
        Exception:  For any unexpected errors during agent processing.

    Example:
        $ poetry run python app.py --main_turns 5 --research_turns 20
    """
    # Parse CLI arguments for max turns for agents
    parser = argparse.ArgumentParser(description="CLI Chat Application")
    parser.add_argument(
        "--main_turns",
        type=int,
        default=3,
        help="Max turns for the main agent (default: 3)",
    )
    parser.add_argument(
        "--research_turns",
        type=int,
        default=15,
        help="Max turns for the research agent (default: 15)",
    )
    args = parser.parse_args()

    try:
        with open("templates/system_message.jinja2", "r") as file:
            system_message = jinja2.Template(file.read()).render(
                current_date=datetime.now().strftime("%d-%m-%Y")
            )
    except Exception as e:
        print(f"Error reading system_message template: {e}")
        sys.exit(1)

    # Initialise the conversation object and add the system message
    conversation = Conversation()
    conversation.add_message("system", system_message)

    # Create the report tool (used as a terminating/fallback tool when needed)
    write_report = Report(terminating=True)

    # Create and configure the research agent with relevant tools
    research_agent = Agent(
        name="research_agent",
        description="This agent is designed to autonomously carry out market research.",
        tools=[Search(), Extract(), Reasoning(), write_report],
        max_turns=args.research_turns,
        terminating=True,
        fallback_tool=write_report,
    )

    # Create the respond tool to handle direct communication
    respond = Respond(response_types=["respond", "clarification"])

    # Set up the main agent with its tools, including the research agent
    main_agent = Agent(
        name="main_agent",
        description="This agent is designed to help users with market research.",
        tools=[Reasoning(), respond, research_agent],
        max_turns=args.main_turns,
        terminating=True,
        fallback_tool=respond,
    )

    console = Console()
    console.print("[bold magenta]Market Research Agent[/bold magenta]")
    console.print(
        "Type your message and press Enter to chat.\n"
        "Special commands: [bold green]reset[/bold green] to clear conversation (system message is retained), "
        "[bold red]exit[/bold red] or [bold red]quit[/bold red] to exit the chat."
    )

    # Main chat loop
    while True:
        try:
            # Prompt the user for input
            user_input = Prompt.ask("[bold green]You[/bold green]")
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            console.print("\n[bold red]Exiting the chat. Goodbye![/bold red]")
            break

        # Check for exit command
        if user_input.strip().lower() in ["exit", "quit"]:
            console.print("[bold red]Exiting the chat. Goodbye![/bold red]")
            break

        # Special command to reset the conversation (keeping the system message)
        if user_input.strip().lower() == "reset":
            if conversation.messages:
                # Keep only the first message (system message) in the conversation
                conversation.messages = [conversation.messages[0]]
            else:
                conversation.messages = []
            console.print("[bold yellow]Conversation has been reset.[/bold yellow]")
            continue

        # Add the user's message to the conversation
        conversation.add_message("user", user_input)
        console.print("[bold blue]Agent is thinking...[/bold blue]")

        try:
            # Run the main agent to get a response
            response = main_agent.run(conversation)
        except Exception as e:
            console.print(f"[bold red]Error during agent processing: {e}[/bold red]")
            continue

        # Add the agent's response to the conversation and display it
        conversation.add_message("assistant", response)
        console.print("[bold blue]Agent:[/bold blue]")
        console.print(Markdown(response))


if __name__ == "__main__":
    main()
