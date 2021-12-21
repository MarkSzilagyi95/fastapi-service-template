from typing import List, Optional, Union

from fastapi import APIRouter, Request

from app.demo.dto.DemoDto import DemoDto
from app.demo.dto.DemoNotFoundDto import DemoNotFoundDto
from app.demo.dto.DemoPayloadDto import DemoPayloadDto
from app.demo.service.DemoService import DemoService
from app.utils.auth.Authentication import Authentication
from app.utils.helpers.ConfigReader import Config

demo = APIRouter()

auth = Authentication()


@demo.get('/', response_model=List[DemoDto])
@auth.basic(credentials=Config('api.credential').get())
# @auth.keycloak(client_id="amapi-clients", realm_name='amapi', role='fire-read')
async def get_name(request: Request):
    service = DemoService()
    return service.get_names()


@demo.get('/mandant')
@auth.basic(credentials=Config('api.credential').get())
# @auth.keycloak(client_id="amapi-clients", realm_name='amapi', role='fire-read')
async def get_name(request: Request):
    service = DemoService()
    return service.get_mandants()


@demo.post('/', status_code=201, response_model=Union[DemoDto, DemoNotFoundDto])
# @auth.basic(credentials=users)
@auth.keycloak(client_id="amapi-clients", realm_name='amapi', role='fire-read')
async def add_name(request: Request, payload: Optional[DemoPayloadDto] = None):
    service = DemoService()
    return service.get_names()
