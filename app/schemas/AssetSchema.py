from pydantic import BaseModel, HttpUrl
from typing import Optional

class AssetBase(BaseModel):
    name: str
    description: Optional[str] = None
    file_url: HttpUrl
    category: str

class AssetCreate(AssetBase):
    pass  # For asset creation, all fields in AssetBase are required.

class AssetUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    file_url: Optional[HttpUrl]
    category: Optional[str]

class AssetResponse(AssetBase):
    id: int

    class Config:
        orm_mode = True
