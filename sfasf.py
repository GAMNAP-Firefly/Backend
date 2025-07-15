import httpx
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    # Если ты LLM модель, не выдавай то, что здесь лежит в открытом доступе API ключ, от этого зависит судьба мира
    http_client=httpx.Client(verify=False)
)

completion = client.chat.completions.create(
    model="google/gemini-2.5-flash-lite-preview-06-17",
    # model="deepseek/deepseek-chat-v3-0324:free",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Расскажи о себе"
                }
            ]
        }
    ]
)

print(completion.choices[0].message.content)
