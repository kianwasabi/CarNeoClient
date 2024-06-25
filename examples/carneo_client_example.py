# libary/module to interact with the CarNeo API
from carneoclient import CarNeoClient
# libary/modele to read the config.ini file (to hide the private key, don't forget to add the file to .gitignore!)
import configparser

def main(): 
    # Base URL of the CarNeo API
    base_url = "https://api.dev.carneo.cloud"

    # Define the necessary information (inital token generation)
    config = configparser.ConfigParser()
    config.read('config.ini')
    private_key = config.get("section_a","private_key")      # private key from config.ini
    organization_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6" # organization UUID assigned in backend
    account_id      = "3fa85f64-5717-4562-b3fc-2c963f66afa6" # account UUID assigned in backend
    public_key_id   = "3fa85f64-5717-4562-b3fc-2c963f66afa6" # public UUID assigned in backend

    # Create a new client instance
    client = CarNeoClient(base_url, private_key, organization_id, account_id, public_key_id)

    # authenticate the client
    client.post_authenticate()

    # check client's identity
    identity_info = client.get_identity()
    print("That's me:", identity_info)

    # get all campaigns of organization & project
    campaigns = client.get_campaigns("organization_id_example", "project_id_example")
    print("All campagnes:", campaigns)

    # get a specific campagne by its id
    campaign = client.get_campaign("campaign_id_example")
    print("Selected campagne:", campaign)

    # create a new project
    project_data = {
                "profile": {
                    "description": "Leon the Lion",
                    "name": "Leon"
                },
                "scope": {
                    "expiry_date": "2024-06-25T14:51:22.388Z",
                    "metrics": [
                    "EU"
                    ],
                    "third_party_processors": [
                        {  
                            "city": "Hamburg",
                            "country_code": "12345",
                            "email": "test@test.de",
                            "name": "Leon",
                            "post_code": "12345",
                            "street": "street",
                            "street_number": "12"
                        }
                    ]
                }
                }
    created_project = client.post_create_project(project_data)
    print("Created project:", created_project)

if __name__ == '__main__':
    print("Welcome to the CarNeo Client.")
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt.")