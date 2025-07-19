# miniature-waffle
My experience with LLMs portfolios

## Pandas DataFrame Agent with Ollama

This repository now includes a small utility module `pandas_ollama_agent.py`
that demonstrates how to build a LangChain agent for working with pandas data
frames powered by an Ollama-hosted language model.

The helper ``create_ollama_llm`` instantiates ``ChatOllama`` from
``langchain_community``, so the agent uses a chat-oriented interface.

`data.csv` in this repository provides a tiny example dataset so you can try
out the agent immediately.

```python
import pandas as pd
from pandas_ollama_agent import (
    create_ollama_llm,
    create_dataframe_agent,
    query_dataframe,
)

df = pd.read_csv("data.csv")
llm = create_ollama_llm()
agent = create_dataframe_agent(df, llm, verbose=True)
response = query_dataframe(agent, "What is the average value in column A?")
print(response)
```

## VSCode Coding Assistant

The `code_assistant_server.py` module exposes a FastAPI server that can answer
questions about code snippets using an Ollama LLM. A minimal VSCode extension
located in `vscode-extension/` sends the selected code to this server and shows
the response in an output channel.

Start the API server:

```bash
python code_assistant_server.py
```

Then install the extension dependencies and launch the extension host from the
`vscode-extension` folder:

```bash
npm install
```

Run the **Ask Ollama Assistant** command and enter a question when prompted to
query the model with the selected code.
