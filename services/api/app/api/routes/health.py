"""Health check endpoints."""

from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check(db: Annotated[Session, Depends(get_db)]) -> dict[str, str]:
    """Check API and Database health."""
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {e}"

    return {
        "status": "ok",
        "database": db_status
    }
