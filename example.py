from libs.carneoclient import CarNeoClient

def main(): 
    # Define the necessary information. 
    base_url = "https://api.dev.carneo.cloud"               # base url of the CarNeo API
    with open('private_key.txt', 'r') as file: 
        private_key = file.read()                            # example private key of the client // to do: .pem file, HS256 or RS256? 
    organization_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6" # example organization UUID assigned in backend
    account_id      = "3fa85f64-5717-4562-b3fc-2c963f66afa6" # example account UUID assigned in backend
    public_key_id   = "3fa85f64-5717-4562-b3fc-2c963f66afa6" # example public UUID assigned in backend
    campaign_id     = "3fa85f64-5717-4562-b3fc-2c963f66afa6" # example campaign UUID assigned in backend
    project_id      = "3fa85f64-5717-4562-b3fc-2c963f66afa6" # example project UUID assigned in backend
    # example project data
    project_data = {
        "profile": {
            "description": "string",
            "name": "string"
        },
        "scope": {
            "expiry_date": "2024-06-30T09:49:00.344Z",
            "metrics": [
                "string"
            ],
            "third_party_processors": [
                {
                    "city": "string",
                    "country_code": "string",
                    "email": "string",
                    "name": "string",
                    "post_code": "string",
                    "street": "string",
                    "street_number": "string"
                }
            ]
        }
    }

    # Create a new client instance.
    client = CarNeoClient(base_url, private_key, organization_id, account_id, public_key_id)

    # Authenticate the client.
    client.authenticate() # to do! -> Check requieremnts for the JWT token.

    # Get client's identity.
    client.bearer_token = 'Bearer ey..'  # workarround due to open to dos in authenticate(): set the bearer token manually from Swagger UI
    identity_info = client.get_identity() 
    print(f"-> That's me: {identity_info}")

    # # Get campaigns of organization and project by it's ID.
    # campaign = client.get_campaign_by_id(project_id, campaign_id) 
    # campaign = client.get_campaign_by_id(project_id, campaign_id, "3fa85f64-5717-4562-b3fc-2c963f66afa6") # with optional organization_id
    # print(f"-> Selected campagne: {campaign}")

    # # Get campaigns of organization and project by pagination. 
    # campaign = client.get_campaign_pagination(project_id) # 
    # print(f"-> Selected campagne: {campaign}")
    # campaign = client.get_campaign_pagination(project_id, 1) # with optional pagination courser 
    # print(f"-> Selected campagne: {campaign}")
    # campaign = client.get_campaign_pagination(project_id, 2, "3fa85f64-5717-4562-b3fc-2c963f66afa6") # with optional organization_id
    # print(f"-> Selected campagne: {campaign}")
    
    # # Create a new project
    # created_project = client.create_project(project_data)
    # print("Created project:", created_project)

if __name__ == '__main__':
    try:
        print("------- CarNeo Client -------")
        main()
        print("-----------------------------")
    except KeyboardInterrupt:
        print("------- KeyboardInterrupt ------- ")