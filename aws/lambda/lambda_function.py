import json
import os
import requests
import datetime
import logging

crypto_pair_contract_addresses = {
    "1INCH/ETH": "0x72AFAECF99C9d9C8215fF44C77B94B99C28741e8",
    "1INCH/USD": "0xc929ad75B72593967DE83E7F7Cda0493458261D9",
    "AAVE/ETH": "0x6Df09E975c830ECae5bd4eD9d90f3A95a4f88012",
    "AAVE/USD": "0x547a514d5e3769680Ce22B2361c10Ea13619e8a9",
    "ADA/USD": "0xAE48c91dF1fE419994FFDa27da09D5aC69c30f55",
    "ALCX/ETH": "0x194a9AaF2e0b67c35915cD01101585A33Fe25CAa",
    "AMPL/ETH": "0x492575FDD11a0fCf2C6C719867890a7648d526eB",
    "APE/ETH": "0xc7de7f4d4C9c991fF62a07D18b3E31e349833A18",
    "APE/USD": "0xD10aBbC76679a20055E167BB80A24ac851b37056",
    "AUD/USD": "0x77F9710E7d0A19669A13c055F62cd80d313dF022",
    "AVAX/USD": "0xFF3EEb22B5E3dE6e705b44749C2559d704923FD7",
    "BADGER/ETH": "0x58921Ac140522867bf50b9E009599Da0CA4A2379",
    "BAL/ETH": "0xC1438AA3823A6Ba0C159CfA8D98dF5A994bA120b",
    "BAL/USD": "0xdF2917806E30300537aEB49A7663062F4d1F2b5F",
    "BAT/ETH": "0x0d16d4528239e9ee52fa531af613AcdB23D88c94",
    "BNB/USD": "0x14e613AC84a31f709eadbdF89C6CC390fDc9540A",
    "BTC/ETH": "0xdeb288F737066589598e9214E782fa5A8eD689e8",
    "BUSD/ETH": "0x614715d2Af89E6EC99A233818275142cE88d1Cfd",
    "BUSD/USD": "0x833D8Eb16D306ed1FbB5D7A2E019e106B960965A",
    "CAD/USD": "0xa34317DB73e77d453b1B8d04550c44D10e981C8e",
    "CAKE/USD": "0xEb0adf5C06861d6c07174288ce4D0a8128164003",
    "CBETH/ETH": "0xF017fcB346A1885194689bA23Eff2fE6fA5C483b",
    "CHF/USD": "0x449d117117838fFA61263B61dA6301AA2a88B13A",
    "CNY/USD": "0xeF8A4aF35cd47424672E3C590aBD37FBB7A7759a",
    "COMP/ETH": "0x1B39Ee86Ec5979ba5C322b826B3ECb8C79991699",
    "COMP/USD": "0xdbd020CAeF83eFd542f4De03e3cF0C28A4428bd5",
    "CRV/ETH": "0x8a12Be339B0cD1829b91Adc01977caa5E9ac121e",
    "CRV/USD": "0xCd627aA160A6fA45Eb793D19Ef54f5062F20f33f",
    "CRVUSD/USD": "0xEEf0C605546958c1f899b6fB336C20671f9cD49F",
    "CVX/ETH": "0xC9CbF687f43176B302F03f5e58470b77D07c61c6",
    "CVX/USD": "0xd962fC30A72A84cE50161031391756Bf2876Af5D",
    "DAI/ETH": "0x773616E4d11A78F511299002da57A0a94577F1f4",
    "DAI/USD": "0xAed0c38402a5d19df6E4c03F4E2DceD6e29c1ee9",
    "DOGE/USD": "0x2465CefD3b488BE410b941b1d4b2767088e2A028",
    "DOT/USD": "0x1C07AFb8E2B827c5A4739C6d59Ae3A5035f28734",
    "ENJ/ETH": "0x24D9aB51950F3d62E9144fdC2f3135DAA6Ce8D1B",
    "ENS/USD": "0x5C00128d4d1c2F4f652C267d7bcdD7aC99C16E16",
    "ETH/BTC": "0xAc559F25B1619171CbC396a50854A3240b6A4e99",
    "ETH/USD": "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419",
    "EUR/USD": "0xb49f677943BC038e9857d61E7d053CaA2C1734C1",
    "EURT/USD": "0x01D391A48f4F7339aC64CA2c83a07C22F95F587a",
    "FIL/ETH": "0x0606Be69451B1C9861Ac6b3626b99093b713E801",
    "FTM/ETH": "0x2DE7E4a9488488e0058B95854CC2f7955B35dC9b",
    "FXS/USD": "0x6Ebc52C8C1089be9eB3945C4350B68B8E4C2233f",
    "GBP/USD": "0x5c0Ab2d9b5a7ed9f470386e82BB36A3613cDd4b5",
    "GRT/ETH": "0x17D054eCac33D91F7340645341eFB5DE9009F1C1",
    "GRT/USD": "0x86cF33a451dE9dc61a2862FD94FF4ad4Bd65A5d2",
    "HBAR/USD": "0x38C5ae3ee324ee027D88c5117ee58d07c9b4699b",
    "IMX/USD": "0xBAEbEFc1D023c0feCcc047Bff42E75F15Ff213E6",
    "JPY/USD": "0xBcE206caE7f0ec07b545EddE332A47C2F75bbeb3",
    "KNC/ETH": "0x656c0544eF4C98A6a98491833A89204Abb045d6b",
    "KNC/USD": "0xf8fF43E991A81e6eC886a3D281A2C6cC19aE70Fc",
    "KRW/USD": "0x01435677FB11763550905594A16B645847C1d0F3",
    "LDO/ETH": "0x4e844125952D32AcdF339BE976c98E22F6F318dB",
    "LINK/ETH": "0xDC530D9457755926550b59e8ECcdaE7624181557",
    "LINK/USD": "0x2c1d072e956AFFC0D435Cb7AC38EF18d24d9127c",
    "LTC/USD": "0x6AF09DF7563C363B5763b9102712EbeD3b9e859B",
    "MANA/ETH": "0x82A44D92D6c329826dc557c5E1Be6ebeC5D5FeB9",
    "MATIC/USD": "0x7bAC85A8a13A4BcD8abb3eB7d6b4d632c5a57676",
    "MKR/ETH": "0x24551a8Fb2A7211A25a17B1481f043A8a8adC7f2",
    "MKR/USD": "0xec1D1B3b0443256cc3860e24a46F108e699484Aa",
    "MLN/ETH": "0xDaeA8386611A157B08829ED4997A8A62B557014C",
    "NZD/USD": "0x3977CFc9e4f29C184D4675f4EB8e0013236e5f3e",
    "PAXG/ETH": "0x9B97304EA12EFed0FAd976FBeCAad46016bf269e",
    "PERP/ETH": "0x3b41D5571468904D4e53b6a8d93A6BaC43f02dC9",
    "PERP/USD": "0x01cE1210Fe8153500F60f7131d63239373D7E26C",
    "RDNT/USD": "0x393CC05baD439c9B36489384F11487d9C8410471",
    "REN/ETH": "0x3147D7203354Dc06D9fd350c7a2437bcA92387a4",
    "RETH/ETH": "0x536218f9E9Eb48863970252233c8F271f554C2d0",
    "RPL/USD": "0x4E155eD98aFE9034b7A5962f6C84c86d869daA9d",
    "RSR/USD": "0x759bBC1be8F90eE6457C44abc7d443842a976d02",
    "SAND/USD": "0x35E3f7E558C04cE7eEE1629258EcbbA03B36Ec56",
    "SGD/USD": "0xe25277fF4bbF9081C75Ab0EB13B4A13a721f3E13",
    "SHIB/ETH": "0x8dD1CD88F43aF196ae478e91b9F5E4Ac69A97C61",
    "SNX/ETH": "0x79291A9d692Df95334B1a0B3B4AE6bC606782f8c",
    "SNX/USD": "0xDC3EA94CD0AC27d9A86C180091e7f78C683d3699",
    "SOL/USD": "0x4ffC43a60e009B551865A93d232E33Fce9f01507",
    "SPELL/USD": "0x8c110B94C5f1d347fAcF5E1E938AB2db60E3c9a8",
    "STETH/ETH": "0x86392dC19c0b719886221c78AB11eb8Cf5c52812",
    "STETH/USD": "0xCfE54B5cD566aB89272946F602D76Ea879CAb4a8",
    "STG/USD": "0x7A9f34a0Aa917D438e9b6E630067062B7F8f6f3d",
    "SUSHI/ETH": "0xe572CeF69f43c2E488b33924AF04BDacE19079cf",
    "SUSHI/USD": "0xCc70F09A6CC17553b2E31954cD36E4A2d89501f7",
    "SXP/USD": "0xFb0CfD6c19e25DB4a08D8a204a387cEa48Cc138f",
    "TRIBE/ETH": "0x84a24deCA415Acc0c395872a9e6a63E27D6225c8",
    "TRY/USD": "0xB09fC5fD3f11Cf9eb5E1C5Dba43114e3C9f477b5",
    "TUSD/ETH": "0x3886BA987236181D98F2401c507Fb8BeA7871dF2",
    "TUSD/USD": "0xec746eCF986E2927Abd291a2A1716c940100f8Ba",
    "UNI/ETH": "0xD6aA3D25116d8dA79Ea0246c4826EB951872e02e",
    "UNI/USD": "0x553303d460EE0afB37EdFf9bE42922D8FF63220e",
    "USDC/ETH": "0x986b5E1e1755e3C2440e960477f25201B0a8bbD4",
    "USDC/USD": "0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6",
    "USDD/USD": "0x0ed39A19D2a68b722408d84e4d970827f61E6c0A",
    "USDP/USD": "0x09023c0DA49Aaf8fc3fA3ADF34C6A7016D38D5e3",
    "USDT/ETH": "0xEe9F2375b4bdF6387aa8265dD4FB8F16512A1d46",
    "USDT/USD": "0x3E7d1eAB13ad0104d2750B8863b489D65364e32D",
    "WBTC/BTC": "0xfdFD9C85aD200c506Cf9e21F1FD8dd01932FBB23",
    "WING/USD": "0x134fE0a225Fb8e6683617C13cEB6B3319fB4fb82",
    "XAG/USD": "0x379589227b15F1a12195D3f2d90bBc9F31f95235",
    "XAU/USD": "0x214eD9Da11D2fbe465a6fc601a91E62EbEc1a0D6",
    "XCN/USD": "0xeb988B77b94C186053282BfcD8B7ED55142D3cAB",
    "YFI/ETH": "0x7c5d4F8345e66f68099581Db340cd65B078C41f4",
    "YFI/USD": "0xA027702dbb89fbd58938e4324ac03B58d812b0E1",
    "ZRX/ETH": "0x2Da4983a622a8498bb1a21FaE9D8F6C664939962"    
}

def lambda_handler(event, context):
    logger = logging.getLogger()
    # Extract slots from Lex event
    print("FULL EVENT INFO")
    print(event)
    crypto_base = event['interpretations'][0]['intent']['slots']['cryptoBase']['value']['originalValue']
    crypto_target = event['interpretations'][0]['intent']['slots']['cryptoTarget']['value']['originalValue']
    crypto_pair = f"{crypto_base.upper()}/{crypto_target.upper()}"
    
    # Check if both cryptoBase and cryptoTarget are provided
    if not crypto_base or not crypto_target:
        return close(event, 'Fulfilled', 'Please provide both base and target cryptocurrencies.')

    # Prepare API query
    contract_address = crypto_pair_contract_addresses[crypto_pair]
    task_ip = "10.0.0.7"
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
        initial_price = int(response_data['rounds'][-1]['answer'])
        decimals = int(response_data['decimals'])
        latest_price = initial_price / (10 ** decimals)
        message = f"The latest price for {crypto_pair} is: {latest_price}"
    except (IndexError, KeyError):
        message = "Could not parse the price information from the response."
        logger.error("Failed to parse price info from user response")

    return close(event, 'Fulfilled', message)

def close(event, fulfillment_state, message):
    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": "CheckPrice",
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message,
            },
        ],
        "requestAttributes": {}
    }

    return response
