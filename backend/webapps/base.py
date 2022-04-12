from fastapi import APIRouter
from webapps.auth import route_login
from webapps.dependencies import route_dependencies
from webapps.users import route_users


api_router = APIRouter()
api_router.include_router(
    route_dependencies.router, prefix="", tags=["dependency-webapp"]
)
api_router.include_router(route_users.router, prefix="", tags=["users-webapp"])
api_router.include_router(route_login.router, prefix="", tags=["auth-webapp"])
