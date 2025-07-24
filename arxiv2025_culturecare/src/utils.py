import csv
import json
from collections import defaultdict

import pandas as pd


def xlsx_to_jsonl(xlsx_file_path, jsonl_file_path, sheet_name=0):
    """
    Convert an XLSX file to a JSONL file.
    """
    # Read the Excel file
    df = pd.read_excel(xlsx_file_path, sheet_name=sheet_name)

    # Convert DataFrame rows to JSON Lines and write to file
    with open(jsonl_file_path, 'w', encoding='utf-8') as jsonl_file:
        for record in df.to_dict(orient='records'):
            jsonl_file.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(f"Successfully converted '{xlsx_file_path}' to '{jsonl_file_path}'.")


def _extract_list(row, max_item, phrase_key, category_key, entry, output_category_key="type"):
    for i in range(1, max_item):
        phrase = row.get(f'{phrase_key}_{i}', "")
        category = row.get(f'{category_key}_{i}', "")
        if isinstance(phrase, str) and phrase.strip() and phrase != "x":
            entry.append({
                "phrase": phrase.strip(),
                 output_category_key: category
            })


def simplify_and_convert_excel_to_jsonl(xlsx_file_path, jsonl_file_path, culture, max_item=8):
    df = pd.read_excel(xlsx_file_path, sheet_name="Export")
    output = []
    for _, row in df.iterrows():
        entry = {
            "culture": culture,
            "post_id": row["post_id"],
            "post": {
                "text": row["post"],
                "emotional_distress": [],
                "cultural_signals": [],
                "demographic_info": [],
            },
            "response": {
                "text": row["response"],
                "emotional_support": [],
                "cultural_signals": [],
                "demographic_info": [],
            }
        }

        # Process emotional distress phrases and intensities
        _extract_list(row, max_item, "emotional_distress", "emotional_distress_intensity",
                                      entry["post"]["emotional_distress"], output_category_key="intensity")
        # Process cultural signals (first block)
        _extract_list(row, max_item, "post_cultural_signal", "post_cultural_signal_type",
                                      entry["post"]["cultural_signals"], output_category_key="type")
        # Process emotional support phrases
        _extract_list(row, max_item, "emotional_support", "emotional_support_strategy",
                                      entry["response"]["emotional_support"], output_category_key="strategy")
        # Handle repeated cultural signals (second block)
        _extract_list(row, max_item, "response_cultural_signal", "response_cultural_signal_type",
                                      entry["response"]["cultural_signals"], output_category_key="type")
        output.append(entry)

    # Write to JSONL
    with open(jsonl_file_path, 'w', encoding='utf-8') as f:
        for item in output:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')


def convert_jsonl_to_csv(input_file, output_file):
    data = []
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            if line:
                try:
                    record = json.loads(line)
                    data.append(record)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    continue

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(data)
