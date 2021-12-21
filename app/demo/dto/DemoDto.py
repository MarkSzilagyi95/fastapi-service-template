from pydantic import BaseModel


class DemoDto(BaseModel):
    id: int
    name: str = None
