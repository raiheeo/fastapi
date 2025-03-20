from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .models import UserProfile 
from .database import get_db  
from authlib.integrations.starlette_client import OAuth


oauth = OAuth()

oauth.register(
    name='google',
    client_id='your-google-client-id',
    client_secret='your-google-client-secret',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:8000/auth/google/callback',
    client_kwargs={'scope': 'openid profile email'},
)

router = APIRouter()


@router.get("/auth/google")
async def login_via_google():
    redirect_uri = 'http://localhost:8000/auth/google/callback'
    return await oauth.google.authorize_redirect(redirect_uri)

@router.get("/auth/google/callback")
async def auth_via_google_callback(db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token()
    userinfo = token.get('userinfo')
    if not userinfo:
        raise HTTPException(status_code=400, detail="Failed to fetch user info")

    email = userinfo.get('email')
    username = userinfo.get('name')
    user = db.query(UserProfile).filter(UserProfile.email == email).first()

    if not user:

        user = UserProfile(
            username=username,
            email=email,
            hashed_password="", 
            first_name=userinfo.get('given_name'),
            last_name=userinfo.get('family_name'),
            status="client"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return {"access_token": "your-access-token", "token_type": "bearer"}