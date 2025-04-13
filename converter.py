import os
import json
import re
from parser import parse_football_txt

def sanitize_filename(name):
    """Remove/replace characters that are unsafe for filenames."""
    return re.sub(r'[\\/:"*?<>|]', '_', name)

def convert_txts_to_jsons(input_root='.', output_dir='./parsed_json'):
    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(input_root):
        for filename in files:
            if filename.endswith('.txt'):
                input_path = os.path.join(root, filename)
                try:
                    with open(input_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    parsed = parse_football_txt(content)
                    if not parsed or not parsed.get("matchdays"):
                        print(f"⚠️  Skipped (no matchdays): {input_path}")
                        continue

                    league = parsed.get("league", "Unknown League")
                    season = parsed.get("season", "Unknown Season")
                    league_safe = sanitize_filename(league)
                    season_safe = sanitize_filename(season)

                    json_filename = f"({season_safe}) {league_safe}.json"
                    output_path = os.path.join(output_dir, json_filename)

                    with open(output_path, 'w', encoding='utf-8') as out_f:
                        json.dump(parsed, out_f, indent=2, ensure_ascii=False)

                except Exception as e:
                    print(f"❌ Error parsing {input_path}: {e}")

    print(f'\n📁 All JSON files saved in: {output_dir}')


if __name__ == '__main__':
    convert_txts_to_jsons(input_root='./', output_dir='./parsed_json')
