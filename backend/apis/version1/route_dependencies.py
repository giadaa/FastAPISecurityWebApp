from typing import List

from apis.version1.route_login import get_current_user_from_token
from db.models.users import User
from db.repository.dependencies import create_new_dependency
from db.repository.dependencies import delete_dependency_by_id
from db.repository.dependencies import list_dependencies
from db.repository.dependencies import retreive_dependency
from db.repository.dependencies import update_dependency_by_id
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from schemas.dependencies import DependencyCreate
from schemas.dependencies import ShowDependency
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create-dependency/", response_model=ShowDependency)
def create_dependency(
    dependency: DependencyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    dependency = create_new_dependency(
        dependency=dependency, db=db, owner_id=current_user.id
    )
    return dependency


@router.get("/get/{id}", response_model=ShowDependency)
def read_dependency(id: int, db: Session = Depends(get_db)):
    dependency = retreive_dependency(id=id, db=db)
    if not dependency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dependency with this id {id} does not exist",
        )
    return dependency


@router.get("/all", response_model=List[ShowDependency])
def read_dependencies(db: Session = Depends(get_db)):
    dependencies = list_dependencies(db=db)
    return dependencies


@router.post("/update/{id}")
def update_dependency(
    id: int,
    dependency: DependencyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    message = update_dependency_by_id(
        id=id, dependency=dependency, db=db, owner_id=current_user.id
    )
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dependency with id {id} not found",
        )
    return {"msg": "Successfully updated data."}


@router.delete("/delete/{id}")
def delete_dependency(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    dependency = retreive_dependency(id=id, db=db)
    if not dependency:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dependency with {id} does not exist",
        )
    if dependency.owner_id == current_user.id or current_user.is_superuser:
        delete_dependency_by_id(id=id, db=db)
        return {"detail": "Successfully deleted."}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You can only delete items that you have created, unless you are an admin.",
    )
