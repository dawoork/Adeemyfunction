import azure.functions as func
import logging
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.oauth2 import service_account
import os
import json
from azure.storage.blob import BlobServiceClient

def get_ga4_client():
    credentials_info = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS_JSON'])
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    client = BetaAnalyticsDataClient(credentials=credentials)
    return client

def upload_to_blob_storage(data):
    blob_service_client = BlobServiceClient.from_connection_string(os.environ['BLOB_CONNECTION_STRING'])
    container_name = os.environ['BLOB_CONTAINER_NAME']
    blob_client = blob_service_client.get_blob_client(container=container_name, blob='ga4_data.json')
    blob_client.upload_blob(data, overwrite=True)

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="AdeemyFuntionAds")
def AdeemyFuntionAds(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "Keeeev. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )