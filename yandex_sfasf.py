import json

import requests

API_KEY = ""
FOLDER_ID = ""

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Api-Key {API_KEY}"
}

body = {
    "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
    "completionOptions": {
        "stream": False,
        "temperature": 0.8,
        "maxTokens": 100
    },
    "messages": [{"role": "user", "text": "Расскажи о себе, кто ты и что можешь"}]
}

response = requests.post(
    "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
    headers=headers,
    data=json.dumps(body)
)

text = response.json()['result']['alternatives'][0]['message']['text']

print(text)
