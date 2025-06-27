from pydantic import BaseModel, Field


class Department(BaseModel):
    id: int
    name: str


class Location(BaseModel):
    id: int
    name: str


class DateInfo(BaseModel):
    datetime: str
    formatted: str


class User(BaseModel):
    id: int
    name: str
    employee_num: str | None = Field(None, alias="employee_num")
    department: Department | None = None
    location: Location | None = None
    assets_count: int


class UserSearchResponse(BaseModel):
    total: int
    rows: list[User]
