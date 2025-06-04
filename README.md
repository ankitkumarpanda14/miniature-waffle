# miniature-waffle
My experience with LLMs portfolios

## Pandas DataFrame Agent with Ollama

This repository now includes a small utility module `pandas_ollama_agent.py`
that demonstrates how to build a LangChain agent for working with pandas data
frames powered by an Ollama-hosted language model.

```python
import pandas as pd
from pandas_ollama_agent import (
    create_ollama_llm,
    create_dataframe_agent,
    query_dataframe,
)

df = pd.read_csv("data.csv")
llm = create_ollama_llm()
agent = create_dataframe_agent(df, llm)
response = query_dataframe(agent, "What is the average value in column A?")
print(response)
```
