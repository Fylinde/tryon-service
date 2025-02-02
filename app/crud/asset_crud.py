from sqlalchemy.orm import Session
from app.models.AssetModel import AssetModel
from app.schemas.AssetSchema import AssetCreate, AssetUpdate

def create_asset(db: Session, asset: AssetCreate):
    new_asset = AssetModel(**asset.dict())
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset

def update_asset(db: Session, asset_id: int, asset: AssetUpdate):
    db_asset = db.query(AssetModel).filter(AssetModel.id == asset_id).first()
    if db_asset:
        for key, value in asset.dict(exclude_unset=True).items():
            setattr(db_asset, key, value)
        db.commit()
        db.refresh(db_asset)
    return db_asset
