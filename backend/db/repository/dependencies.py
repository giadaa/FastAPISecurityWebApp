from db.models.dependencies import Dependency
from schemas.dependencies import DependencyCreate
from sqlalchemy.orm import Session


def create_new_dependency(dependency: DependencyCreate, db: Session, owner_id: int):
    dependency_object = Dependency(**dependency.dict(), owner_id=owner_id)
    db.add(dependency_object)
    db.commit()
    db.refresh(dependency_object)
    return dependency_object


def retreive_dependency(id: int, db: Session):
    item = db.query(Dependency).filter(Dependency.id == id).first()
    return item


def list_dependencies(db: Session):
    dependency = db.query(Dependency).all()
    return dependency


def update_dependency_by_id(
    id: int, dependency: DependencyCreate, db: Session, owner_id: int
):
    existing_dependency = db.query(Dependency).filter(Dependency.id == id)
    if not existing_dependency.first():
        return 0
    dependency.__dict__.update(
        owner_id=owner_id
    )  # update dictionary with new key value of owner_id
    existing_dependency.update(dependency.__dict__)
    db.commit()
    return 1


def delete_dependency_by_id(id: int, db: Session):
    existing_dependency = db.query(Dependency).filter(Dependency.id == id)
    if not existing_dependency.first():
        return 0
    existing_dependency.delete(synchronize_session=False)
    db.commit()
    return 1
