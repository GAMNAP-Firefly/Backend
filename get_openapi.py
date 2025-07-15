#!/usr/bin/env python3
"""
Скрипт для получения OpenAPI спецификации и конвертации в YAML.
"""

import requests
import yaml


def get_openapi_yaml():
    """Получает OpenAPI спецификацию и конвертирует в YAML."""
    server_url = "https://localhost:8443"

    try:
        # Получаем OpenAPI JSON
        response = requests.get(server_url + "/openapi.json", verify=False)
        response.raise_for_status()

        # Парсим JSON
        openapi_data = response.json()

        # Конвертируем в YAML
        yaml_content = yaml.dump(openapi_data, default_flow_style=False, sort_keys=False, allow_unicode=True)

        # Сохраняем в файл
        with open("openapi.yaml", "w", encoding="utf-8") as f:
            f.write(yaml_content)

        print("✅ OpenAPI спецификация сохранена в openapi.yaml")
        print(f"📄 Размер файла: {len(yaml_content)} символов")

    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения к серверу. Убедитесь, что сервер запущен на " + server_url)
    except Exception as e:
        print(f"❌ Ошибка: {e}")


get_openapi_yaml()
