from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.asset_crud import create_asset, update_asset
from app.schemas.AssetSchema import AssetCreate, AssetResponse, AssetUpdate

router = APIRouter()



@router.post("/assets/", response_model=AssetResponse)
def create_new_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    return create_asset(db, asset)

@router.put("/assets/{asset_id}", response_model=AssetResponse)
def update_existing_asset(asset_id: int, asset: AssetUpdate, db: Session = Depends(get_db)):
    db_asset = update_asset(db, asset_id, asset)
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset
