from db.base_class import Base
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Dependency(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # title
    latest_version = Column(String, nullable=False)  # company
    deadline = Column(Date, nullable=False)  # location
    date_posted = Column(Date)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="dependencies")
