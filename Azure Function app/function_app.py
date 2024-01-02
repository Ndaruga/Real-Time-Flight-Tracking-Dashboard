import logging
import requests
import azure.functions as func
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.identity import ClientSecretCredential


app = func.FunctionApp()

@app.schedule(schedule="0 0/10 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger_10_mins(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    
    vault_url='https://flightdatasecretkey.vault.azure.net/'
    key_vault_name = vault_url.split('.')[0].split('/')[2]

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    secretName='FLIGHT-API-KEY'
    API_KEY = client.get_secret(secretName)
    BASE_URL = f"https://airlabs.co/api/v9/flight?api_key={API_KEY}"
    
    try:
        # Fetch data from the API
        response = requests.get(BASE_URL)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

        # Parse JSON response
        data = response.json()
        if data is not " ":
            logging.info("Data available")
        else:
            logging.error("No data")
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from the API: {e}")

    logging.info('Python timer trigger function executed.')