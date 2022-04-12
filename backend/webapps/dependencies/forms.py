from datetime import date
from typing import List
from typing import Optional

from fastapi import Request


class DependencyCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.name: Optional[str] = None
        self.latest_version: Optional[str] = None
        self.deadline: Optional[date] = None

    async def load_data(self):
        form = await self.request.form()
        self.name = form.get("name")
        self.latest_version = form.get("latest_version")
        self.deadline = form.get("deadline")

    def is_valid(self):
        if not self.name or not len(self.name) >= 1:
            self.errors.append("A valid dependency name is required")
        if not self.latest_version or not len(self.latest_version) >= 1:
            self.errors.append("A valid latest_version is required")
        if not self.errors:
            return True
        return False
