from pydantic import BaseModel
from typing import Dict, Any, Optional

class ScrapingResponse(BaseModel):
    status: str
    data: Any
    source: str  # "live" ou "cache"
    error: Optional[str] = None