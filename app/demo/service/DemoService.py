from app.demo.dto.DemoPayloadDto import DemoPayloadDto
from app.demo.model.DemoModel import DemoModel


class DemoService:
    def __init__(self):
        pass

    def get_mandants(self):
        mandants = DemoModel().mandant()
        return mandants.to_dict(orient='records')

    @classmethod
    def get_names(cls):
        return [{"id": 1, "name": "fastapi", "comment": "my test comment"},
                {"id": 2, "name": "fastapi 2", "comment": "my test comment"}]

    @classmethod
    def add_names(cls, payload: DemoPayloadDto):
        if payload is None:
            return {"message": "not found", "description": "the element cannot be found!"}
        else:
            return payload.dict()
