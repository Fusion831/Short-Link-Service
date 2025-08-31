import secrets
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse


import models
import schemas
from database import get_db, engine

models.Base.metadata.create_all(bind = engine)
#Creates the Database tables based on the models we made in schemas, but Alembic already handles this, I put it here cuz learning fr.



app = FastAPI()


@app.get('/')
async def read_root():
    return {"Message":"ShortLink Service is working."}


@app.post('/shorten', response_model=schemas.UrlInfo)
async def shorten_url(url: schemas.UrlCreate, db: Session = Depends(get_db)):
    short_code = secrets.token_urlsafe(8)  # random 8 letter string
    db_url = models.URL(
        long_url=url.long_url,
        short_code=short_code
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url) #Gives data of the new object
    short_link = f'http://localhost:8000/{short_code}'
    return {
        "long_url": db_url.long_url,
        "short_link" : short_link
    }

