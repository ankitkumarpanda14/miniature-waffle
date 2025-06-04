import pandas as pd
from pandas_ollama_agent import create_ollama_llm, create_dataframe_agent, query_dataframe


df = pd.read_csv("data.csv")
llm = create_ollama_llm()
agent = create_dataframe_agent(df, llm, verbose=True)
response = query_dataframe(agent, "What is the maximum value of all the columns?")
print(response)
