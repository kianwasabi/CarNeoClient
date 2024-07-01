import requests
import jwt
from datetime import datetime, timezone, timedelta
import logging

class CarNeoClient:
    def __init__(self, base_url, private_key, organization_id, account_id, public_key_id):
        self.base_url = base_url
        # Authentication
        self.private_key = private_key
        self.organization_id = organization_id
        self.account_id = account_id
        self.public_key_id = public_key_id
        self.bearer_token = None                # Format: 'Bearer eyJraWQiOiI3..'
        self.bearer_token_expiry = None         # Format: '2024-06-25T14:51:22.388Z'
        # Identity
        # self.subject = None
        # self.provider = None
        # self.iam_identity = None
        # logging 
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            #level=logging.DEBUG,
            datefmt='%H:%M:%S'
            )
    
    def _generate_jwt(self) -> str:
        ''' (private) Generate a JSON web token for the client.
        Param: None
        Returns: token (str)
        '''
        # create timestamp for iat (issued at) & exp (expires at)
        now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z') # Current timestamp in UTC with Z suffix
        than = datetime.strptime(now, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=1) # Parse to datetime object & Add 1 hour
        exp = than.isoformat() + 'Z' # Format to ISO 8601 with Z suffix

        # create payload for jwt
        payload = {
            "org": str(self.organization_id),
            "acc": str(self.account_id),
            "key": str(self.public_key_id),
            "iat": str(now),
            "exp": str(exp)
        }
        
        # generate jwt token (see: https://pyjwt.readthedocs.io/en/latest/)
        try: 
            jwt_token = jwt.encode(payload, self.private_key, algorithm="HS256") 
            logging.info(f"Generated JWT: {jwt_token}")
            return jwt_token 
        except Exception as err:
            logging.error(err)
            return None
    
    def authenticate(self) -> None:
        ''' Authenticate the client with a JSON web token at the server. 
        Receives and sets the client's bearer token and bearer token expiry.
        This method should be called before any other method.
        Param: None
        Returns: None
        '''
        url = f"{self.base_url}/service_accounts/:authenticateServiceAccount" 
        headers = {'accept': 'application/json', 
                   'Content-Type': 'application/json'}
        jwt_token = self._generate_jwt() 
        payload = {"auth_token": jwt_token}
        try: 
            response = requests.post(url, headers=headers, json = payload)
            response.raise_for_status()
            self.bearer_token = response.json()["bearer_token"] 
            self.bearer_token_expiry = response.json()["expiry"]
        except Exception as err:
            logging.error(f"{err} | Response: {response.json().get('message')}")

    def get_identity(self) -> dict:
        ''' Get client's identity from the Server defined by the bearer token.
        Param: None
        Returns: identity_info:dict -> {subject:str,provider:str,iam_identity:str}
        '''
        url = f"{self.base_url}/auth/own_identity"
        headers = {'accept': 'application/json', 
                   'Authorization': self.bearer_token}
        try: 
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            identity_info = response.json()
            # self.subject = identity_info["subject"]
            # self.provider = identity_info["provider"]
            # self.iam_identity = identity_info["iam_identity"]
            return identity_info
        except Exception as err:
            logging.error(f"{err} | Response: {response.json()}")
            return None
        
    def get_campaign_by_id(self, project_id:str, campaign_id:str, organization_id:str = None) -> dict:
        '''Get campaigns for an organization & project by campaign id. 
        Param: project (str), campaign_id (str), organization_id(str) default: self.organization_id
        Returns: campaigns (dict)
        '''
        if organization_id is None: 
            organization_id = self.organization_id
        url = f"{self.base_url}/campaigns/{organization_id}/{project_id}/{campaign_id}"
        headers = {'accept': 'application/json', 
                   'Authorization': self.bearer_token}
        try: 
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            campaign = response.json()
            return campaign
        except Exception as err:
            logging.error(f"{err} | Response: {response.json().get('message')}")
            return None
       
    def get_campaign_pagination(self, project_id:str, cursor:str=None, organization_id:str = None) -> dict:
        '''Get campaigns for an organization and project with optional cursor for pagination. 
        Param: project_id (str), cursor (str) optional , organization_id(str) optional default: self.organization_id
        Returns: campaigns (dict)
        '''
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
        if organization_id is None: 
            organization_id = self.organization_id
        url = f"{self.base_url}/projects/{organization_id}"
        headers = {'accept': 'application/json', 
                   'Content-Type': 'application/json'}
        try:
            response = requests.post(url, headers=headers, json=project_data)
            response.raise_for_status()
            created_project = response.json()
            return created_project
        except Exception as err:
            logging.error(f"{err} | Response: {response.json().get('message')}")
            return None
