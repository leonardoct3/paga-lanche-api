from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RunBase(BaseModel):
    score: int = Field(ge=0)
    duration: int = Field(ge=0, description="Duration in seconds")


class RunCreate(RunBase):
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str = Field(min_length=1, max_length=80)


class RunRead(RunBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    created_at: datetime
