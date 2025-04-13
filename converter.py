import os
import json
from parser import parse_football_txt  # assumes this function exists and works correctly

def split_competition_name(name):
    """
    Splits competition name into league and season.
    Example: 'English Premier League 2024/25' -> ('English Premier League', '2024/25')
    """
    if not name:
        return "Unknown League", "Unknown Season"

    parts = name.rsplit(' ', 1)
    if len(parts) == 2 and '/' in parts[1]:
        return parts[0], parts[1]
    return name, "Unknown Season"

def convert_all_to_single_json(input_root='.', output_file='./all_matches.json'):
    all_data = []

    for root, _, files in os.walk(input_root):
        for filename in files:
            if filename.endswith('.txt'):
                input_path = os.path.join(root, filename)
                try:
                    with open(input_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    parsed = parse_football_txt(content)
                    if not parsed:
                        print(f"⚠️  Skipped (empty parsing): {input_path}")
                        continue

                    competition = parsed.get('competition')
                    league, season = split_competition_name(competition)

                    all_data.append({
                        "league": league,
                        "season": season,
                        "matchdays": parsed.get("matchdays", [])
                    })
                    print(f'Parsed: {input_path}')
                except Exception as e:
                    print(f"❌ Error parsing {input_path}: {e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f'\n✅ All data saved to {output_file}')

if __name__ == '__main__':
    convert_all_to_single_json(input_root='./', output_file='./all_matches.json')