import logging
import json
import os
import requests
import azure.functions as func
from dotenv import load_dotenv

parent_folder = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(parent_folder, '.env')

load_dotenv(dotenv_path)
ML_ENDPOINT = os.environ.get("ML_ENDPOINT")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing a prediction request.")

    try:
        # parse incoming json data
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON input.", status_code=400)

    # prepare headers for ml service call
    headers = {'Content-Type': 'application/json'}
    
    # prepare payload for ml endpoint 
    payload = json.dumps({"data": req_body.get("data")})
    
    # call api
    response = requests.post(ML_ENDPOINT, data=payload, headers=headers)
    
    # return ml endpoint response
    return func.HttpResponse(response.text, status_code=response.status_code, mimetype="application/json")
