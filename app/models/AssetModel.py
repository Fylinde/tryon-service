from sqlalchemy import Column, Integer, String, Text
from app.database import BaseModel

class AssetModel(BaseModel):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    file_url = Column(String, nullable=False)  # URL of the 3D asset file
    category = Column(String, index=True)  # Category (e.g., "fashion", "home decor")
