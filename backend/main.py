from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api.accounts import router as accounts_router
from api.analytics import router as analytics_router
from api.media import router as media_router
from api.setup import router as setup_router
from middleware.auth.simple_auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 インスタグラムアナリティクスAPI Starting...")
    yield
    print("📊 インスタグラムアナリティクスAPI Shutting down...")

app = FastAPI(
    title="Instagram Analytics API",
    description="Instagram分析アプリのバックエンドAPI",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["認証"])
app.include_router(accounts_router, prefix="/accounts", tags=["アカウント管理"])
app.include_router(analytics_router, prefix="/analytics", tags=["分析データ"])
app.include_router(media_router, prefix="/media", tags=["投稿データ"])
app.include_router(setup_router, tags=["セットアップ"])

@app.get("/")
async def root():
    return {
        "message": "Instagram Analytics API", 
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )