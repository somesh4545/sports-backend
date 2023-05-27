from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.index import Organizers
from schemas.index import Organizer
from sqlalchemy.orm import Session 
from fastapi import Depends
from config.db import get_db

organizerssRouter = APIRouter()

@organizerssRouter.get('/')
async def fetch_all_org(db: Session = Depends(get_db)):
    return db.query(Organizers).all()

@organizerssRouter.post('/')
async def create_org(org: Organizer, db: Session = Depends(get_db)):
    org_item = Organizers(name=org.name, email=org.email)
    db.add(org_item)
    db.commit()
    db.refresh(org_item)
    return org_item

@organizerssRouter.get('/{id}')
async def get_org_by_id(id, db: Session = Depends(get_db)):
    org = db.query(Organizers).filter(Organizers.id == id).first()
    if org is None:
        raise HTTPException(status_code=404, detail="No organization found")
    return org


