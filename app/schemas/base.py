from datetime import datetime

from pydantic import BaseModel


class TimestampResponse(BaseModel):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True