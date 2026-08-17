from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent import agente_proceso

app = FastAPI(title="ADK Agent GCS PDF Service")


class QueryRequest(BaseModel):
    prompt: str


@app.get("/")
def health_check():
    return {"status": "ok", "service": "ADK Agent PDF Reader"}


@app.post("/ask")
async def ask_agent(request: QueryRequest):
    try:
        response = agente_proceso.run(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
