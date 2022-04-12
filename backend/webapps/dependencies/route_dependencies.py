from apis.version1.route_login import get_current_user_from_token
from apis.version1.route_login import is_user_logged_in
from db.models.users import User
from db.repository.dependencies import create_new_dependency
from db.repository.dependencies import list_dependencies
from db.repository.dependencies import retreive_dependency
from db.repository.dependencies import update_dependency_by_id
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from schemas.dependencies import DependencyCreate
from sqlalchemy.orm import Session
from webapps.dependencies.forms import DependencyCreateForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    token = request.cookies.get("access_token")
    _, param = get_authorization_scheme_param(token)
    is_logged_in = is_user_logged_in(token=param, db=db)
    if not is_logged_in:
        return responses.RedirectResponse(
            url="/login/", status_code=303, headers={"content-type": "text/html"}
        )
    dependencies = list_dependencies(db=db)
    user = get_current_user_from_token(token=param, db=db)
    return templates.TemplateResponse(
        "general_pages/homepage.html",
        {
            "request": request,
            "dependencies": dependencies,
            "msg": msg,
            "is_authenticated": is_logged_in,
            "user": user.username,
        },
    )


@router.get("/post-a-dependency/")
def create_dependency(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    _, param = get_authorization_scheme_param(token)
    is_logged_in = is_user_logged_in(token=param, db=db)
    user = get_current_user_from_token(token=param, db=db)
    return templates.TemplateResponse(
        "dependencies/create_dependencies.html",
        {"request": request, "is_authenticated": is_logged_in, "user": user.username},
    )


@router.post("/post-a-dependency/")
async def create_dependency(request: Request, db: Session = Depends(get_db)):
    form = DependencyCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            _, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            current_user: User = get_current_user_from_token(token=param, db=db)
            dependency = DependencyCreate(**form.__dict__)
            dependency = create_new_dependency(
                dependency=dependency, db=db, owner_id=current_user.id
            )
            return responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)
        except Exception as e:
            if isinstance(e, ValueError):
                form.__dict__.get("errors").append(e)
            else:
                form.__dict__.get("errors").append(
                    "You might not be logged in, In case problem persists please contact us."
                )
            return templates.TemplateResponse(
                "dependencies/create_dependencies.html", form.__dict__
            )
    return templates.TemplateResponse(
        "dependencies/create_dependencies.html", form.__dict__
    )


@router.post("/update/{id}")
async def update_dependency(request: Request, db: Session = Depends(get_db)):
    form = DependencyCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            _, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            current_user: User = get_current_user_from_token(token=param, db=db)
            updated_dependency = DependencyCreate(**form.__dict__)
            id = request.path_params["id"]
            existing_dependency = retreive_dependency(id=id, db=db)
            if (
                existing_dependency.owner_id == current_user.id
                or current_user.is_superuser
            ):
                update_dependency_by_id(
                    id=id,
                    dependency=updated_dependency,
                    db=db,
                    owner_id=current_user.id,
                )
                return responses.RedirectResponse(
                    "/", status_code=status.HTTP_302_FOUND
                )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You can only delete items that you have created, unless you are an admin.",
            )

        except Exception as e:
            if isinstance(e, HTTPException):
                form.__dict__.get("errors").append(e.detail)
            else:
                form.__dict__.get("errors").append(
                    "You might not be logged in, In case problem persists please contact us."
                )
            print(form.__dict__.items())
            return templates.TemplateResponse(
                "general_pages/homepage.html", form.__dict__
            )
    return templates.TemplateResponse("general_pages/homepage.html", form.__dict__)
