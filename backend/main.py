from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title = "Speech-LLM Quality Lab API")

#Cors authorizing react frontend
app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# TODO: include routers step for step
# from backend.routers import asr, llm_cases
# app.include_router(asr.router, prefix="/api/asr")
