from dotenv import load_dotenv
import os
from openai import OpenAI
import json

load_dotenv()

api_key = os.getenv('OPENAI_KEY')
os.environ['OPENAI_API_KEY'] = api_key

client = OpenAI()

query =  "send 10 eth to Josh at 0x12348782112344123"

response = client.responses.create(
    model="gpt-4o-2024-08-06",
    input=[
        {"role": "system", "content": "Detect the action the user is trying to perform."},
        {"role": "user", "content": query}
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "action",
            "schema": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "The action is determined by the type of transaction that the user wishes to perform. This can be a swap, a normal sending funds transaction, or a bridge transaction",
                        "enum": ["swap", "send_funds", "bridge"]
                    },
                    "amount": {
                        "type": "number",
                        "description": "The amount of tokens that the user wishes to use for the transaction"
                    },
                    "token":{
                    	"type": "string",
                    	"description": "The token that the user wants to send, swap or bridge",
                    	"enum": ["ETH", "BSC", "POL", "USDC", "Other"]
                    },
                    "network": {
                    	"type": "string",
                    	"description": "The network that the user wants to perform the transaction on. If it's a bridge, this is the network that the funds will be sent from.",
                    	"enum": ["Ethereum", "Binance Smart Chain", "Polygon", "Other"]
                    },
                    "to_token":{
                    	"type": ["string", "null"],
                    	"description": "The token that the user wants to swap into - only applicable when user performs a swap.",
                    	"enum": ["ETH", "BSC", "POL", "USDC", "Other"]
                    },
                    "to_network": {
						"type": ["string", "null"],
                    	"description": "If applicable, the network that the user wants to bridge onto",
                    	"enum": ["Ethereum", "Binance Smart Chain", "Polygon", "Other"]
                    },
                    "to_address": {
                        "type": ["string", "null"], 
                        "description": "The public address that the user wants to send the funds to. Starts with 0x. In case of a swap, this is null."
                    },
                },
                "required": ["action", "amount", "token", "network", "to_token", "to_network", "to_address"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
)

event = json.loads(response.output_text)

print(event)