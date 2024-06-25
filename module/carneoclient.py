import requests
import jwt
import datetime

class CarNeoClient:
    def __init__(self, base_url, private_key, organization_id, account_id, public_key_id):
        self.base_url = base_url
        self.private_key = private_key
        self.organization_id = organization_id
        self.account_id = account_id
        self.public_key_id = public_key_id
        self.bearer_token = None
        self.bearer_token_expiry = None
    
    def _generate_jwt(self):
        ''' Generate a JSON web token for the client.
        Param: None
        Returns: token (str)
        '''
        now = datetime.now()
        # iat: issued at, exp: expiration time (iat+1h)
        payload = {
            'org': self.organization_id,
            'acc': self.account_id,
            'key': self.public_key_id,
            'iat': now,                                     
            'exp': now + datetime.timedelta(hours=1)
        }
        jwt_token = jwt.encode(payload, self.private_key, algorithm='RS256') # https://pyjwt.readthedocs.io/en/latest/
        return jwt_token 


    def post_authenticate(self):
        ''' Authenticate the client with a JSON web token at the server. 
            Stores the bearer token & expiry in the client instance.
        Param: None
        Returns: None
        '''
        # curl -X 'POST' \
        # 'https://api.dev.carneo.cloud/service_accounts/:authenticateServiceAccount' \
        # -H 'accept: application/json' \
        # -H 'Content-Type: application/json' \
        # -d '{"auth_token": "string"}'
        # 200: "bearer_token": "string", "expiry": "string" (ISO 8601 format)
        url = f"{self.base_url}/service_accounts/:authenticateServiceAccount" 
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        jwt_token = self._generate_jwt() 
        payload = {"auth_token": jwt_token}
        response = requests.post(url, headers=headers, json = payload)
        response.raise_for_status()
        self.bearer_token = response.json()["bearer_token"]
        self.bearer_token_expiry = response.json()["expiry"]

    def get_identity(self):
        ''' Authenticate the client with the server. 
            Stores the bearer token in the client instance.
        Param: None
        Returns: JSON encoded (UFT-8)
        '''
        # curl -X 'GET'
        # 'https://api.dev.carneo.cloud/auth/own_identity' 
        # -H 'accept: application/json'
        # 200: "subject": "string", "provider": "string", "iam_identity": "string"
        url = f"{self.base_url}/auth/own_identity"
        headers = {'accept': 'application/json'}
        #headers = {'accept': 'application/json', 'Authorization': self.bearer_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_campaign(self, campaign_id):
        # Abruf einer einzelnen “Campaign” unter Zuhilfenahme der CampaignID
        url = f"{self.base_url}/campaigns/{campaign_id}"
        response = requests.get(url, headers=self._check_headers())
        response.raise_for_status()
        return response.json()

    def get_campaigns(self, organization_id, project_id):
        #Abruf der „Campaigns“ nach Organization und Project
        url = f"{self.base_url}/campaigns/{organization_id}/{project_id}"
        campaigns = []
        cursor = None
        while True:
            params = {}
            if cursor:
                params['cursor'] = cursor
            response = requests.get(url, headers=self._check_headers(), params=params)
            response.raise_for_status()
            data = response.json()
            campaigns.extend(data['campaigns'])
            cursor = data.get('next_cursor')
            if not cursor:
                break
        return campaigns
    
    def post_create_project(self, project_data):
        # Erstellen eines „Projects“
        url = f"{self.base_url}/projects"
        response = requests.post(url, headers=self._check_headers(), json=project_data)
        response.raise_for_status()
        return response.json()