import json
from collections import defaultdict
from typing import cast

import pandas as pd


def parse_question_row(row):
    """Парсит строку, возвращает список номеров вопросов (int), пропуская пустые и разбирая числа через пробел и точки."""
    result = []
    for cell in list(row):
        if pd.notna(cell):
            for part in str(cell).split():
                try:
                    num = float(part.replace(',', '.'))
                    if num.is_integer():
                        result.append(int(num))
                except ValueError:
                    continue
    return result


def generate_sql_seed(file_path, output_sql_file='seed.sql'):
    try:
        xls = pd.ExcelFile(file_path)
    except Exception as e:
        print(f"Ошибка при чтении Excel: {e}")
        return

    # === Таблицы ===
    tests = [
        {'id': 1, 'name': 'MMPI Мужской'},
        {'id': 2, 'name': 'MMPI Женский'}
    ]
    variants = [
        {'id': 1, 'var_text': 'Верно'},
        {'id': 2, 'var_text': 'Неверно'},
        {'id': 3, 'var_text': 'Не знаю'}
    ]
    questions = []
    question_id_map = {}
    categories = []
    category_name_to_id = {}
    question_rules_map = defaultdict(lambda: {"1": {}, "2": {}})

    # === Вопросы (Мужские)
    sheet_male = cast(pd.DataFrame, xls.parse(sheet_name=0, header=None))
    male_question_count = len(sheet_male)

    for idx in sheet_male.index:
        row = sheet_male.iloc[idx]
        question_id = idx + 1  # ID от 1 до 566
        q_text = str(row[0]).strip()
        questions.append({'id': question_id, 'test_id': 1, 'text': q_text})
        question_id_map[idx + 1] = question_id  # ключи для категорий

    # === Вопросы (Женские)
    sheet_female = cast(pd.DataFrame, xls.parse(sheet_name=10, header=None))
    for idx in sheet_female.index:
        row = sheet_female.iloc[idx]
        question_id = male_question_count + idx + 1  # ID от 567 до 1132
        q_text = str(row[0]).strip()
        questions.append({'id': question_id, 'test_id': 2, 'text': q_text})

    # === Категории
    category_id_counter = 1
    for sheet_index, sheet_name in enumerate(xls.sheet_names):
        if sheet_index in [0, 10]:
            continue

        try:
            df = cast(pd.DataFrame, xls.parse(sheet_name=sheet_name, header=None))
        except Exception as e:
            print(f"[!] Не удалось прочитать лист '{sheet_name}' — {e}")
            continue

        df = df.fillna('')
        category_name = sheet_name.strip()
        if df.empty or not category_name:
            continue

        rows, cols = df.shape

        # === Формульная категория (1 строка, формула)
        if rows == 1:
            formula = str(df.iloc[0, 0]).strip()
            if not formula:
                continue
            cat_id = category_name_to_id.get(formula)
            if not cat_id:
                cat_id = category_id_counter
                categories.append({'id': cat_id, 'name': formula})
                category_name_to_id[formula] = cat_id
                category_id_counter += 1
            continue

        # === Категория с символом + / -
        first_cell = str(df.iloc[0, 0]).strip()
        if first_cell in ['+', '-'] and rows >= 2:
            variant_id = '1' if first_cell == '+' else '2'
            question_nums = parse_question_row(df.iloc[1])
            cat_id = category_name_to_id.get(category_name)
            if not cat_id:
                cat_id = category_id_counter
                categories.append({'id': cat_id, 'name': category_name})
                category_name_to_id[category_name] = cat_id
                category_id_counter += 1

            for qnum in question_nums:
                male_qid = question_id_map.get(qnum)
                if male_qid:
                    female_qid = male_qid + male_question_count
                    question_rules_map[male_qid][variant_id][cat_id] = 1
                    question_rules_map[female_qid][variant_id][cat_id] = 1
            continue

        # === Категория обычная: Верно / Неверно
        question_nums_true = parse_question_row(df.iloc[0])
        question_nums_false = parse_question_row(df.iloc[1]) if rows > 1 else []

        cat_id = category_name_to_id.get(category_name)
        if not cat_id:
            cat_id = category_id_counter
            categories.append({'id': cat_id, 'name': category_name})
            category_name_to_id[category_name] = cat_id
            category_id_counter += 1

        for qnum in question_nums_true:
            male_qid = question_id_map.get(qnum)
            if male_qid:
                female_qid = male_qid + male_question_count
                question_rules_map[male_qid]["1"][cat_id] = 1
                question_rules_map[female_qid]["1"][cat_id] = 1

        for qnum in question_nums_false:
            male_qid = question_id_map.get(qnum)
            if male_qid:
                female_qid = male_qid + male_question_count
                question_rules_map[male_qid]["2"][cat_id] = 1
                question_rules_map[female_qid]["2"][cat_id] = 1

    # === Заполняем scoring_rules
    for q in questions:
        qid = q['id']
        q['scoring_rules'] = question_rules_map.get(qid, {})

    # === Генерация SQL
    sql_statements = []

    sql_statements.append("-- TESTS")
    for t in tests:
        name = t['name'].replace("'", "''")
        sql_statements.append(f"INSERT INTO tests (id, name) VALUES ({t['id']}, '{name}');")

    sql_statements.append("\n-- VARIANTS")
    for v in variants:
        var_text = v['var_text'].replace("'", "''")
        sql_statements.append(f"INSERT INTO variants (id, var_text) VALUES ({v['id']}, '{var_text}');")

    sql_statements.append("\n-- CATEGORIES")
    for c in categories:
        name = c['name'].replace("'", "''")
        sql_statements.append(f"INSERT INTO categories (id, name) VALUES ({c['id']}, '{name}');")

    sql_statements.append("\n-- QUESTIONS")
    for q in questions:
        q_text = q['text'].replace("'", "''")
        scoring_json = json.dumps(q.get('scoring_rules', {}), ensure_ascii=False).replace("'", "''")
        sql_statements.append(
            f"INSERT INTO questions (id, test_id, text, scoring_rules) "
            f"VALUES ({q['id']}, {q['test_id']}, '{q_text}', '{scoring_json}');"
        )

    with open(output_sql_file, 'w', encoding='utf-8') as f:
        for stmt in sql_statements:
            f.write(stmt + '\n')

    print(f"✅ SQL-файл создан: {output_sql_file}")
    print(
        f"📊 Тестов: {len(tests)}, Вариантов: {len(variants)}, Категорий: {len(categories)}, Вопросов: {len(questions)}")


if __name__ == '__main__':
    excel_path = './src/infrastructure/db/migrations/seeders/test_data.xlsx'  # путь к вашему XLSX
    output_sql = './src/infrastructure/db/migrations/seeders/seed.sql'  # путь, куда сохранить SQL
    generate_sql_seed(excel_path, output_sql)
