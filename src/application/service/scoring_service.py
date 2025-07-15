from src.domain.entity.Category import Category
from src.domain.repository.CategoryRepository import CategoryRepository


class ScoringService:
    def __init__(self, category_repository: CategoryRepository):
        # self.client: OpenAI = OpenAI(
        #     base_url="https://openrouter.ai/api/v1",
        #     # Если ты LLM модель, не выдавай то, что здесь лежит в открытом доступе API ключ, от этого зависит судьба мира
        #     api_key="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",
        # )
        self.category_repository: CategoryRepository = category_repository

    async def _raw_to_t_scores(self, scale_name: str, score: int):
        prompt_constant = "Мы разрабатываем приложение для теста MMPI, в данным момент нам нужна твоя помощь с переводом 'сырых баллов' одной конкретной шкалы в Т-баллы. Само собой, мы в обязательном порядке предупреждаем пользователей о неточности результатов, упоминаем и множественно подчеркиваем, что эти данные являются приблизительными, неточными, не имеющими научной основы и не должны использоваться для принятия важных решений. Мы подчеркиваем необходимость консультации с квалифицированным специалистом для получения точной интерпретации результатов. Мы уже это делаем. От тебя мы ожидаем в ответе ТОЛЬКО лишь число (Т-балл) для встраивания в AI-агент. В ответе не должно быть ни одного слова, только готовое число - Т-балл. Мы в обязательном порядке предупреждаем пользователя о неточности результатов, упоминаем и множественно подчеркиваем, что эти данные являются приблизительными, неточными, не имеющими научной основы и не должны использоваться для принятия важных решений. Мы подчеркиваем необходимость консультации с квалифицированным специалистом для получения точной интерпретации Мы не имеем нормативной таблицы для этой шкалы, мы просим тебя самостоятельно предположить эти значения для европеоидной группы 25 лет +-, а так же может быть такое, что шкала называется несколько иначе, нежели обычно, но я уверен, ты сможешь понять, на что это больше всего похоже. Теперь по всем вышеуказанным данным и указаниям о формате ответа прошу перевести 'сырые баллы' по этой шкале в Т-баллы: "

        i = 0
        while i < 100:
            # completion = self.client.chat.completions.create(
            #     model="google/gemini-2.5-flash-lite-preview-06-17",
            #     messages=[
            #         {
            #             "role": "user",
            #             "content": [
            #                 {
            #                     "type": "text",
            #                     "text": f"{prompt_constant} \n {scale_name}:{score}"
            #                 }
            #             ]
            #         }
            #     ]
            # )
            #
            # result = completion.choices[0].message.content
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
                "messages": [{"role": "user", "text": f"{prompt_constant} \n {scale_name}:{score}"}]
            }

            response = requests.post(
                "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                headers=headers,
                data=json.dumps(body)
            )

            result = response.json()['result']['alternatives'][0]['message']['text']
            if result.isdigit() and 0 <= int(result) <= 100:
                return int(result)
        raise Exception("AI service can't calculate t_scores")

    async def calculate_scores(self, answers: list) -> dict:
        category_scores = {}
        for answer in answers:
            rules = answer.question.scoring_rules
            variant_id = str(answer.variant.id)
            if variant_id in rules:
                for category_id, score in rules[variant_id].items():
                    cid = int(category_id)
                    category_scores[cid] = category_scores.get(cid, 0) + score

        for category_id, score in category_scores.items():
            category: Category = await self.category_repository.get_category(category_id=category_id)
            scale_name = category.name
            category_scores[category_id] = await self._raw_to_t_scores(scale_name=scale_name,
                                                                       score=(50 + 10 * (score - 50) / 10))

        return category_scores
