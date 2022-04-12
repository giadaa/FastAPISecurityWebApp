from apis.version1.route_login import get_current_user_from_token
from apis.version1.route_login import is_user_logged_in
from db.repository.users import create_new_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from schemas.users import UserCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from webapps.users.forms import UserCreateForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/register/")
def register(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    _, param = get_authorization_scheme_param(token)
    is_logged_in = is_user_logged_in(token=param, db=db)
    user = None
    if is_logged_in:
        user = get_current_user_from_token(token=param, db=db).username
    return templates.TemplateResponse(
        "users/register.html",
        {"request": request, "is_authenticated": is_logged_in, "user": user},
    )


@router.post("/register/")
async def register(request: Request, db: Session = Depends(get_db)):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreate(
            username=form.username, email=form.email, password=form.password
        )
        try:
            user = create_new_user(user=user, db=db)
            return responses.RedirectResponse(
                "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
            )  # default is post request, to use get request added status code 302
        except IntegrityError:
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse("users/register.html", form.__dict__)
    return templates.TemplateResponse("users/register.html", form.__dict__)
