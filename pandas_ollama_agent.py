"""Utilities to work with pandas DataFrame agents powered by an Ollama LLM."""

from __future__ import annotations

import pandas as pd

from langchain_community.llms import Ollama
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import (
    create_pandas_dataframe_agent,
)


def create_ollama_llm(model: str = "llama3", base_url: str | None = None) -> Ollama:
    """Create an Ollama LLM instance.

    Parameters
    ----------
    model : str
        Name of the ollama model to use.
    base_url : str, optional
        Base URL of the Ollama server. Defaults to ``http://localhost:11434``.
    """
    if base_url is None:
        base_url = "http://localhost:11434"
    return Ollama(model=model, base_url=base_url)


def create_dataframe_agent(
    df: pd.DataFrame,
    llm: Ollama,
    *,
    verbose: bool = False,
    allow_dangerous_code: bool = True,
) -> "AgentExecutor":
    """Create a LangChain pandas DataFrame agent using the provided LLM."""
    return create_pandas_dataframe_agent(
        llm,
        df,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        verbose=verbose,
        allow_dangerous_code=allow_dangerous_code,
    )


def query_dataframe(agent, prompt: str) -> str:
    """Run a natural language query against the DataFrame agent."""
    return agent.run(prompt)


__all__ = [
    "create_ollama_llm",
    "create_dataframe_agent",
    "query_dataframe",
]
