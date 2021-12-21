from typing import Optional

from pydantic import BaseModel


class DemoPayloadDto(BaseModel):
    id: int
    name: Optional[str]
