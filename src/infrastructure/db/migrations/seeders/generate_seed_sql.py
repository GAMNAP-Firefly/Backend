import pandas as pd
from collections import defaultdict
import json
import os

def generate_sql_seed():
    """
    Парсит Excel test_data.xlsx и генерирует SQL-скрипт
    в src/infrastructure/db/migrations/seeders/seed.sql
    """
    # Определяем пути
    script_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..', '..', '..'))
    
    file_path = os.path.join(project_root, 'test_data.xlsx')
    output_sql_file = os.path.join(script_dir, 'seed.sql')

    if not os.path.exists(file_path):
        print(f"❌ Файл '{file_path}' не найден.")
        return

    try:
        xls = pd.ExcelFile(file_path)
    except Exception as e:
        print(f"❌ Ошибка при чтении Excel: {e}")
        print("💡 Убедитесь, что установлен 'openpyxl': pip install openpyxl")
        return

    # === Таблицы ===
    tests = [
        {'id': 1, 'name': 'MMPI Мужской'},
        {'id': 2, 'name': 'MMPI Женский'}
    ]

    variants = [
        {'id': 1, 'var_text': 'Верно'},
        {'id': 2, 'var_text': 'Неверно'}
    ]

    questions = []
    categories = []
    category_name_to_id = {}
    question_rules_map = defaultdict(lambda: {"1": {}, "2": {}})

    # === Вопросы ===
    # Мужские: лист 0
    sheet_male = xls.parse(sheet_name=0)
    for idx, row in sheet_male.iterrows():
        question_id = idx + 1
        q_text = str(row[0]).strip()
        questions.append({
            'id': question_id,
            'test_id': 1,
            'text': q_text
        })

    # Женские: лист 10
    sheet_female = xls.parse(sheet_name=10)
    offset = len(questions)
    for idx, row in sheet_female.iterrows():
        question_id = offset + idx + 1
        q_text = str(row[0]).strip()
        questions.append({
            'id': question_id,
            'test_id': 2,
            'text': q_text
        })

    # === Категории ===
    category_id_counter = 1
    for i, sheet_name in enumerate(xls.sheet_names):
        if i in [0, 10]:
            continue

        df = xls.parse(sheet_name=sheet_name, header=None)
        category_name = sheet_name.strip()

        if not category_name:
            continue

        if category_name not in category_name_to_id:
            category_id = category_id_counter
            category_name_to_id[category_name] = category_id
            categories.append({'id': category_id, 'name': category_name})
            category_id_counter += 1

        category_id = category_name_to_id[category_name]

        # Безопасно читаем A1 (Верно), A2 (Неверно)
        true_row = str(df.iloc[0, 0]) if df.shape[0] > 0 else ""
        false_row = str(df.iloc[1, 0]) if df.shape[0] > 1 else ""

        # "Верно"
        for qnum in true_row.strip(',').split(','):
            qnum = qnum.strip()
            if qnum.isdigit():
                question_rules_map[int(qnum)]["1"][category_id] = 1

        # "Неверно"
        for qnum in false_row.strip(',').split(','):
            qnum = qnum.strip()
            if qnum.isdigit():
                question_rules_map[int(qnum)]["2"][category_id] = 1

    # === Добавляем scoring_rules в вопросы ===
    for q in questions:
        qid = q['id']
        q['scoring_rules'] = question_rules_map.get(qid, {})

    # === Генерация SQL ===
    sql_statements = []

    # Tests
    sql_statements.append("-- TESTS")
    for t in tests:
        name = t['name'].replace("'", "''")
        sql_statements.append(f"INSERT INTO tests (id, name) VALUES ({t['id']}, '{name}');")

    # Variants
    sql_statements.append("\n-- VARIANTS")
    for v in variants:
        var_text = v['var_text'].replace("'", "''")
        sql_statements.append(f"INSERT INTO variants (id, var_text) VALUES ({v['id']}, '{var_text}');")

    # Categories
    sql_statements.append("\n-- CATEGORIES")
    for c in categories:
        cat_name = c['name'].replace("'", "''")
        sql_statements.append(f"INSERT INTO categories (id, name) VALUES ({c['id']}, '{cat_name}');")

    # Questions
    sql_statements.append("\n-- QUESTIONS")
    for q in questions:
        q_text = q['text'].replace("'", "''")
        scoring_json = json.dumps(q.get('scoring_rules', {}), ensure_ascii=False).replace("'", "''")
        sql_statements.append(
            f"INSERT INTO questions (id, test_id, text, scoring_rules) "
            f"VALUES ({q['id']}, {q['test_id']}, '{q_text}', '{scoring_json}');"
        )

    # === Сохраняем SQL в файл ===
    try:
        with open(output_sql_file, 'w', encoding='utf-8') as f:
            for stmt in sql_statements:
                f.write(stmt + '\n')
        print(f"\n✅ SQL-файл успешно создан: {output_sql_file}")
        print(f"🧪 Записано: {len(tests)} тестов, {len(variants)} вариантов, {len(categories)} категорий, {len(questions)} вопросов.")
    except IOError as e:
        print(f"❌ Ошибка при записи seed.sql: {e}")

# Запуск
if __name__ == '__main__':
    generate_sql_seed()