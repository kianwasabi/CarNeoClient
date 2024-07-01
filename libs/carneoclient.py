import requests
import jwt
from datetime import datetime, timezone
import logging

class CarNeoClient:
    def __init__(self, base_url, private_key, organization_id, account_id, public_key_id):
        self.base_url = base_url
        self.private_key = private_key          # Format: 'secret'
        self.organization_id = organization_id  # Format: '3fa85f64-5717-4562-b3fc-2c963f66afa6'
        self.account_id = account_id            # Format: '3fa85f64-5717-4562-b3fc-2c963f66afa6'
        self.public_key_id = public_key_id      # Format: '3fa85f64-5717-4562-b3fc-2c963f66afa6'
        self.bearer_token = None                # Format: 'Bearer eyJraWQiOiI3..'
        self.bearer_token_expiry = None         # Format: '2024-06-25T14:51:22.388Z'
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            #level=logging.DEBUG,
            level=logging.INFO,
            datefmt='%H:%M:%S'
            )
    
    def _generate_jwt(self) -> str:
        '''Generate a JSON web token for the client.
        Param: None
        Returns: token (str)
        '''
        # Claims for JWT (RFC 7519) for the JWT
        iat = int(datetime.now(timezone.utc).timestamp()) # issued at time
        exp = iat + 3600                                  # 1 hour      
        claims = {
            'org': self.organization_id,    # Format: '3fa85f64-5717-4562-b3fc-2c963f66afa6'
            'acc': self.account_id,         # Format: '3fa85f64-5717-4562-b3fc-2c963f66afa6'
            'key': self.public_key_id,      # Format: '3fa85f64-5717-4562-b3fc-2c963f66afa6'
            'iat': iat,                     # Format: 1371720939
            'exp': exp                      # Format: 1371720939
        }
        try: 
            jwt_token = jwt.encode(claims, self.private_key, algorithm="HS256") 
            logging.info(f"Generated JWT.")
            return jwt_token 
        except Exception as err:
            logging.error(err)
            return None

    def _check_token(self) -> None:
        ''' If the bearer token is not set or expired, authenticate the client.
        Param: None
        Returns: None
        '''
        expiry_time = datetime.strptime(self.bearer_token_expiry, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)
        if ((self.bearer_token or self.bearer_token_expiry) is None) or (current_time > expiry_time): 
            logging.info("Bearer token is expired or not set. Authenticate the client.")
            self.authenticate()

    def authenticate(self) -> None:
        ''' Authenticate the client with a JWT. 
        Receives and sets the client's bearer token and bearer token expiry.
        This method should be called before any other method. 
        If the bearer token is expired or not set, this method will be called by the other methods.
        Param: None
        Returns: None
        '''
        url = f"{self.base_url}/service_accounts/:authenticateServiceAccount" 
        headers = {'accept': 'application/json', 
                   'Content-Type': 'application/json'}
        jwt_token = self._generate_jwt() 
        payload = {"auth_token": jwt_token}
        try: 
            response = requests.post(url, headers=headers, json=payload)
            ###### testen ######
            self.bearer_token_expiry = "2024-07-01T15:31:07.416Z" 
            ####################
            response.raise_for_status()
            logging.info(f"Authenticated.")
            self.bearer_token = response.json()["bearer_token"]  
            self.bearer_token_expiry = response.json()["expiry"]
        except Exception as err:
            logging.error(f"{err} | Response: {response.json().get('message')}")

    def get_identity(self) -> dict:
        ''' Get client's identity from the Server defined by the bearer token.
        Param: None
        Returns: identity_info:dict -> {subject:str,provider:str,iam_identity:str}
        '''
        self._check_token()
        url = f"{self.base_url}/auth/own_identity"
        headers = {'accept': 'application/json', 
                   'Authorization': self.bearer_token}
        try: 
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            identity_info = response.json()
            logging.info(f"Got Identity.")
            return identity_info
        except Exception as err:
            logging.error(f"{err} | Response: {response.json()}")
            return None
        
    def get_campaign_by_id(self, project_id:str, campaign_id:str, organization_id:str = None) -> dict:
        '''Get campaigns for an organization & project by campaign id. 
        Param: project (str), campaign_id (str), organization_id(str) default: self.organization_id
        Returns: campaigns (dict)
        '''
        # check if token and is not expired
        self._check_token()
        if organization_id is None: 
            organization_id = self.organization_id
        url = f"{self.base_url}/campaigns/{organization_id}/{project_id}/{campaign_id}"
        headers = {'accept': 'application/json', 
                   'Authorization': self.bearer_token}
        try: 
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            campaign = response.json()
            logging.info(f"Got Campaigns.")
            return campaign
        except Exception as err:
            logging.error(f"{err} | Response: {response.json().get('message')}")
            return None
       
    def get_campaign_pagination(self, project_id:str, cursor:str=None, organization_id:str = None) -> dict:
        '''Get campaigns for an organization and project with optional cursor for pagination. 
        Param: project_id (str), cursor (str) optional , organization_id(str) optional default: self.organization_id
        Returns: campaigns (dict)
        '''
        self._check_token()
        if organization_id is None: 
            organization_id = self.organization_id
        if cursor is None:
            url = f"{self.base_url}/campaigns/{organization_id}/{project_id}"
            # to do: Use get_campaign_by_id here or make a single function for both
        else:
            url = f"{self.base_url}/campaigns/{organization_id}/{project_id}/?cursor={cursor}"
        headers = {'accept': 'application/json', 
                'Authorization': self.bearer_token}
        try: 
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            campaign = response.json()
            logging.info(f"Got Campaigns.")
            return campaign
        except Exception as err:
            logging.error(f"{err} | Response: {response.json().get('message')}")
            return None

    def create_project(self, project_data:dict, organization_id=None) -> dict:
        '''Create a project with the given project data dict for an organization.
        By default, the organization_id is the client's organization_id.
        Param: project_data (dict)
        Returns: created_project (dict)
        '''
        self._check_token()
        if organization_id is None: 
            organization_id = self.organization_id
        url = f"{self.base_url}/projects/{organization_id}"
        headers = {'accept': 'application/json', 
                   'Content-Type': 'application/json'}
        try:
            response = requests.post(url, headers=headers, json=project_data)
            response.raise_for_status()
            created_project = response.json()
            logging.info(f"Created Project.")
            return created_project
        except Exception as err:
            logging.error(f"{err} | Response: {response.json().get('message')}")
            return None
