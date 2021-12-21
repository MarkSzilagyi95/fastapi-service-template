from pydantic import BaseModel


class DemoNotFoundDto(BaseModel):
    message: str
    description: str
