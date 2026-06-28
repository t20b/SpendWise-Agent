from pydantic import BaseModel, ConfigDict


class CategoryRead(BaseModel):
    id: int
    name: str
    is_default: bool

    model_config = ConfigDict(from_attributes=True)
