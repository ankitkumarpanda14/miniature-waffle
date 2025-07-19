"""Simple API server exposing an Ollama-powered code assistant."""

from fastapi import FastAPI
from pydantic import BaseModel
from pandas_ollama_agent import create_ollama_llm
from langchain.schema import HumanMessage

app = FastAPI()
llm = create_ollama_llm()


class Query(BaseModel):
    code: str
    question: str | None = None


@app.post("/query")
async def query_code(data: Query):
    prompt = data.question or "Please review the following code:"\
        + "\n" + data.code
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    # LangChain returns a ChatMessage object with content
    return {"answer": response.content}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
