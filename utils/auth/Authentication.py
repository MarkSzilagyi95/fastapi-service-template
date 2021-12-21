import base64
import functools

from fastapi import HTTPException, status
from fastapi.security import HTTPBasic
from keycloak import KeycloakOpenID

from utils.helpers.ConfigReader import Config

security = HTTPBasic()


class Authentication:

    def keycloak(self, client_id, realm_name, role):

        def inner(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                self._auth_verifier(kwargs)
                authorization = self._get_basic_auth(kwargs)
                username = authorization[0]
                password = authorization[1]
                self._keycloak_login(client_id, realm_name, role, username, password)
                return await func(*args, **kwargs)

            return wrapper

        return inner

    def _keycloak_login(self, client_id, realm_name, role, username, password):
        try:
            keycloak_openid = KeycloakOpenID(server_url=Config('keycloak.url').get(),
                                             client_id=client_id,
                                             realm_name=realm_name,
                                             client_secret_key="")
            token = keycloak_openid.token(username, password)
            # Get Userinfo
            userinfo = keycloak_openid.userinfo(token['access_token'])
        except:
            self._raise_authentication_failed()

        if role not in userinfo['roles']:
            self._raise_resource_not_allowed()

    def _raise_resource_not_allowed(self):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Resource not allowed!",
            headers={"WWW-Authenticate": "Basic"},
        )

    def _raise_authentication_required(self):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required!",
            headers={"WWW-Authenticate": "Basic"},
        )

    def _raise_authentication_failed(self):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed!",
            headers={"WWW-Authenticate": "Basic"},
        )

    def _get_basic_auth(self, keyword_arguments):

        authorization = str(keyword_arguments['request'].headers['authorization']).split(" ")
        username = str(base64.b64decode(authorization[1]).decode()).split(":")[0]
        password = str(base64.b64decode(authorization[1]).decode()).split(":")[1]
        return username, password

    def _auth_verifier(self, keyword_arguments):
        try:
            authorization = str(keyword_arguments['request'].headers['authorization']).split(" ")
            if "Basic" in authorization:
                self.has_auth = True
            else:
                self._raise_authentication_required()
        except:
            self._raise_authentication_required()

    def basic(self, credentials):
        def inner(func):

            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                self._auth_verifier(kwargs)
                authorization = self._get_basic_auth(kwargs)
                username = authorization[0]
                password = authorization[1]

                auth_correct = False
                if username in credentials and credentials.get(username) == password:
                    auth_correct = True
                if not auth_correct:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Authentication failed!",
                        headers={"WWW-Authenticate": "Basic"},
                    )
                return await func(*args, **kwargs)

            return wrapper

        return inner
