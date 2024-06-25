# libary/module to interact with the CarNeo API
from module.carneoclient import CarNeoClient
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
    new_project = {
        "name": "Neues Projekt",
        "description": "Beschreibung des neuen Projekts"
    }
    created_project = client.create_project(new_project)
    print("Created project:", created_project)

if __name__ == '__main__':
    print("Welcome to the CarNeo Client.")
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt.")