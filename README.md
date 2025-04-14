# Minimalist-Agent

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-dependency%20management-brightgreen)](https://python-poetry.org/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A CLI-based autonomous research assistant powered by LLMs.

## Overview

Minimalist-Agent is a command-line application that utilises two specialised AI agents to help with research tasks:

1. **Main Agent**: Interfaces with the user, handles conversations, and delegates research tasks.
2. **Research Agent**: Autonomously performs research using specialised tools.

## Philosophy

The core philosophy of Minimalist-Agent is to achieve elegant simplicity through minimal, clean architecture. The entire system is built around just two fundamental base classes that serve as the foundation for all functionality. This deliberate minimalism reduces complexity, enhances maintainability, and creates a codebase that is both powerful and approachable. By focusing on essential abstractions, the project demonstrates how sophisticated agent behaviours can emerge from a thoughtfully designed, minimalist architecture.

## Features

- Interactive CLI interface with rich text formatting
- Multi-agent architecture for specialised tasks
- Integrated research tools:
  - Web search capabilities via Tavily
  - Data extraction and processing
  - Reasoning capabilities
  - Report generation
- Conversation management
- Configurable agent behaviour

## Requirements

- Python 3.10 - 3.12
- Poetry (dependency management)

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/minimalist-agent.git
   cd minimalist-agent
   ```

2. Install dependencies with Poetry:

   ```
   poetry install
   ```

3. Copy the example environment file and add your API keys:

   ```
   cp .env.example .env
   ```

4. Edit the `.env` file to add your API keys (OpenAI and Tavily).

## Usage

Start the CLI application:

```
poetry run python app.py [--main_turns N] [--research_turns N]
```

### Command-line Arguments

- `--main_turns`: Maximum number of turns the main agent can take (default: 3)
- `--research_turns`: Maximum number of turns the research agent can take (default: 15)

### Commands

- Type your message and press Enter to interact with the agent
- `reset`: Clear the conversation history (retains the system prompt)
- `exit` or `quit`: Exit the application

## Project Structure

- `app.py`: Main application entry point
- `src/`: Core code
  - `agent.py`: Agent implementation
  - `conversation.py`: Conversation management
  - `base.py`: Base classes
  - `tools/`: Tool implementations
    - `search.py`: Web search functionality
    - `extract.py`: Data extraction
    - `reasoning.py`: Reasoning capabilities
    - `respond.py`: Response handling
    - `report.py`: Report generation
- `templates/`: Jinja2 templates for prompts and responses
- `pyproject.toml`: Project configuration and dependencies
