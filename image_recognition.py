from dotenv import load_dotenv
import os
import base64
from openai import OpenAI

load_dotenv()

api_key = os.getenv('OPENAI_KEY')
os.environ['OPENAI_API_KEY'] = api_key

client = OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


image_path = "metamask-images/normal_screen.png"
base64_image = encode_image(image_path)

prompt = """This is a photo of a user's Metamask wallet. Describe what you see in the photo. 

If there is an error make sure to capture it in your description. 

If these details are visible, extract:

 1. the user's public address - this will not be shown if the image depicts a transaction
 2. the tokens that they own
 3. the network that the wallet has selected
 4. if a transaction is shown, the public address that the funds are being sent to and the details of the transaction

If the image is not of the Metamask wallet, describe the error (if any) and what you see in the image.
"""

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                { "type": "text", "text": prompt },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
)

photo_description = completion.choices[0].message.content

print(photo_description)