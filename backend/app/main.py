from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .chatbot import answer_question
from .config import settings
from .retrieval import Retriever
from .schemas import ChatRequest, ChatResponse, Source

app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.allowed_origins.split(",")],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)
retriever = Retriever(settings.data_file)


@app.get("/api/health")
def health():
    return {"status": "ok", "records": len(retriever.records), "model": settings.openrouter_model}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    records = retriever.search(req.message, k=7)
    try:
        answer, mode = await answer_question(req.message, records)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI provider request failed: {type(exc).__name__}") from exc
    sources = []
    seen = set()
    for r in records:
        if r.url not in seen:
            sources.append(Source(title=r.title, url=r.url, provider=r.provider))
            seen.add(r.url)
    return ChatResponse(answer=answer, sources=sources[:5], mode=mode)


@app.post("/api/reload")
def reload_data():
    retriever.reload()
    return {"records": len(retriever.records)}


frontend = Path("frontend/dist")
if frontend.exists():
    app.mount("/assets", StaticFiles(directory=frontend / "assets"), name="assets")

    @app.get("/{path:path}")
    def spa(path: str):
        target = frontend / path
        if path and target.is_file():
            return FileResponse(target)
        return FileResponse(frontend / "index.html")
