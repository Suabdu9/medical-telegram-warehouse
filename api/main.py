from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from sqlalchemy.orm import Session

from typing import List

from api.schemas import (
    TopProduct,
    ChannelActivity,
    SearchResult,
    VisualContent,
)

from api.database import get_db
from api import crud

app = FastAPI(
    title="Medical Telegram Analytics API",
    description="Analytical API for Ethiopian medical Telegram warehouse",
    version="1.0",
)


@app.get(
    "/api/reports/top-products",
    response_model=List[TopProduct],
)
def top_products(
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return crud.top_products(db, limit)


@app.get(
    "/api/channels/{channel_name}/activity",
    response_model=ChannelActivity,
)
def activity(
    channel_name: str,
    db: Session = Depends(get_db),
):

    result = crud.channel_activity(
        db,
        channel_name,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Channel not found",
        )

    return result


@app.get(
    "/api/search/messages",
    response_model=List[SearchResult],
)
def search(
    query: str,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return crud.search_messages(
        db,
        query,
        limit,
    )


@app.get(
    "/api/reports/visual-content",
    response_model=List[VisualContent],
)
def visual(
    db: Session = Depends(get_db),
):
    return crud.visual_content(db)
