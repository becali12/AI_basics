from dotenv import load_dotenv
import os
from openai import OpenAI
import json
import requests

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY')
ETHERSCAN_KEY = os.getenv("ETHERSCAN_KEY")
os.environ['OPENAI_API_KEY'] = OPENAI_KEY

client = OpenAI()

def get_eth_balance(address):
    print(f'Fetching eth balance for address {address}')
    base_url = "https://api.etherscan.io/v2/api"
    
    params = {
        "chainid": "1",
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest",
        "apikey": ETHERSCAN_KEY
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        wei_balance = int(data.get("result", 0))
        eth_balance = wei_balance / 10**18
        return eth_balance
    except requests.RequestException as e:
        print("Error fetching balances:", e)
        return None


def get_eth_price():
    base_url = "https://api.etherscan.io/v2/api"
    print("Getting ETH price")
    params = {
        "chainid": 1,
        "module": "stats",
        "action": "ethprice",
        "tag": "latest",
        "apikey": ETHERSCAN_KEY
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        print("FROM ETHERSCAN PRICE API:", data)
        return data.get("result")
    except requests.RequestException as e:
        print("Error fetching ETH price:", e)
        return None


query = "how much ETH do I have"

tools = [{
    "type": "function",
    "name": "get_eth_balance",
    "description": "Get user's eth balance",
    "parameters": {
        "type": "object",
        "properties": {
            "address": {
                "type": "string",
                "description": "The user's public address. It starts with 0x"
            }
        },
        "required": ["address"],
        "additionalProperties": False
    }
},
# {
#     "type": "function",
#     "name": "get_eth_price",
#     "description": "Get current price of eth",
#     "parameters": {
#     	"type": "object",
#     	"properties": {},
#     	"required": [],
#         "additionalProperties": False
#     }
# }
]

response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "system", "content": "User's public address is 0x7Bf994F1C5869454c2DCba267504E8D521BDc913"},
        {"role": "user", "content": query}
    ],
    tools=tools
)

print(response.output)

response_obj = response.output[0]
function_name = response_obj.name
arguments_dict = json.loads(response_obj.arguments)


if function_name in globals():
    function_to_call = globals()[function_name]
    result = function_to_call(**arguments_dict)
    print("Function Output:", result)
else:
    result = None
    print(f"Function '{function_name}' not found.")

input_messages = [response_obj]
input_messages.append({
    "type": "function_call_output",
    "call_id": response_obj.call_id,
    "output": str(result)
})

response_2 = client.responses.create(
    model="gpt-4o",
    input=input_messages,
    tools=tools,
)

print(response_2.output_text)
