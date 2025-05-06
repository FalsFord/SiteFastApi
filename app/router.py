from fastapi import APIRouter, HTTPException, status, Depends, Response

from app.schemas import SUserRegister, UserBase, SUserAuth
from core.models import crud
from pathlib import Path

from pydantic import EmailStr, BaseModel
from starlette.responses import FileResponse, RedirectResponse

from core.models import db_helper
from fastapi import Request, Depends

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession

BASE_DIR = Path(__file__).resolve().parent.parent

router = APIRouter()
router.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@router.post("/register", response_model=UserBase)
async def register_user(
    user_data: SUserRegister,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_user(session=session, user_in=user_data)


@router.get("/register")
def get_register_page():
    return FileResponse(BASE_DIR / "static" / "register" / "index.html")


@router.get("/profile")
async def get_profile(
    request: Request,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    email_str = request.cookies.get("email")
    if not email_str:
        return RedirectResponse(url="/login", status_code=300)

    try:

        class EmailModel(BaseModel):
            email: EmailStr

        email_model = EmailModel(email=email_str)
        user = await crud.get_user(session=session, email=email_model.email)

    except ValueError as e:
        return RedirectResponse(url="/login", status_code=300)

    profile = Jinja2Templates(directory="static/profile")
    return profile.TemplateResponse("profile.html", {"request": request, "user": user})


@router.get("/login")
def get_login_page():
    return FileResponse(BASE_DIR / "static" / "login" / "login.html")


@router.post("/login")
async def login_user(
    response: Response,
    user_data: SUserAuth,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    email = user_data.email
    password = user_data.password
    user = await crud.get_user(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found!",
        )
    elif password == user.password:
        response.set_cookie(key="email", value=email)
        return user


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("email")
    return RedirectResponse(
        url="/login",
        status_code=303
    )


@router.get("/user/{username}", response_model=UserBase)
async def get_user(
    username: str, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):

    user = await crud.get_user(session=session, username=username)
    if user is not None:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {username} not found!",
    )
