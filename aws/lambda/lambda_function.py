import json
import os
import requests
import datetime
import logging

def lambda_handler(event, context):
    logger = logging.getLogger()
    # Extract slots from Lex event
    crypto_base = event['currentIntent']['slots']['cryptoBase']
    crypto_target = event['currentIntent']['slots']['cryptoTarget']
    
    # Check if both cryptoBase and cryptoTarget are provided
    if not crypto_base or not crypto_target:
        return close(event, 'Fulfilled', 'Please provide both base and target cryptocurrencies.')

    # Prepare API query
    task_ip = "10.0.0.7"
    contract_address = "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"
    current_timestamp = int(datetime.datetime.now().timestamp())
    api_key = os.getenv('API_KEY')  # Retrieve API key from Lambda environment variable
    chain = "mainnet"
    api_endpoint = f"http://{task_ip}:3000/api/price?contractAddress={contract_address}&startTimestamp={current_timestamp}&endTimestamp={current_timestamp}&chain={chain}&rpcUrl={api_key}"

    # Make the API request
    try:
        response = requests.get(api_endpoint)
        response_data = response.json()
    except Exception as e:
        return close(event, 'Fulfilled', f"Error making API request: {str(e)}")

    # Parse the response
    try:
        logger.info("FULL RESPONSE DATA")
        logger.info(response_data)
        initial_price = int(response_data['rounds'][-1]['answer'])
        logger.info("INITIAL PRICE")
        logger.info(initial_price)
        decimals = int(response_data['decimals'])
        logger.info("DECIMALS")
        logger.info(decimals)
        latest_price = initial_price / (10 ** decimals)
        message = f"The latest price for {crypto_base}/{crypto_target} is: {latest_price}"
    except (IndexError, KeyError):
        message = "Could not parse the price information from the response."
        logger.error("Failed to parse price info from user response")

    return close(event, 'Fulfilled', message)

def close(event, fulfillment_state, message):
    response = {
        'sessionAttributes': event['sessionAttributes'],
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }
    return response
