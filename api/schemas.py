from pydantic import BaseModel


class TopProduct(BaseModel):
    product: str
    mentions: int


class ChannelActivity(BaseModel):
    channel: str
    total_messages: int
    total_views: int
    average_views: float


class SearchResult(BaseModel):
    message_id: int
    channel: str
    message_text: str
    views: int


class VisualContent(BaseModel):
    channel: str
    total_images: int
