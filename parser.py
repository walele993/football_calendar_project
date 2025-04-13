import re
from datetime import datetime

def parse_football_txt(content):
    league = None
    season = None
    matchdays = []
    current_matchday = None
    current_date = None
    current_time = None

    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # League and season title
        if line.startswith('= '):
            title_line = line[2:].strip()

            match = re.search(r'(\d{4}/\d{2})$', title_line)
            if match:
                season = match.group(1)
                league = title_line[:match.start()].strip()
            else:
                league = title_line
                season = None
            continue

        # Matchday or round
        matchday_match = None

        if line.startswith('»'):
            matchday_match = re.match(r'» (?:[A-Za-z]+,\s*)?(.+)', line)
        elif re.match(r'(Matchday \d+|[A-Za-z ]+Round \d+|[A-Za-z ]+round|[A-Za-z ]+Finals?)', line):
            matchday_match = re.match(r'(.+)', line)

        if matchday_match:
            if current_matchday:
                matchdays.append(current_matchday)
            current_matchday = {
                "matchday": matchday_match.group(1).strip(),
                "matches": []
            }

        # Date
        date_match = re.match(r'([A-Za-z]{3} [A-Za-z]{3}/\d{2}(?: \d{4})?)', line)
        if date_match:
            try:
                parts = date_match.group(1).split(' ', 1)[1]
                if len(parts.split()[-1]) == 4:
                    current_date = datetime.strptime(parts, '%b/%d %Y').strftime('%Y-%m-%d')
                else:
                    current_date = datetime.strptime(parts + ' 2024', '%b/%d %Y').strftime('%Y-%m-%d')
            except Exception as e:
                print(f"[DEBUG] Error parsing date: {e}")
                current_date = None
            continue

        # Time
        time_match = re.match(r'(\d{1,2}\.\d{2})', line)
        if time_match:
            current_time = time_match.group(1).replace('.', ':')
            line = line[line.find(time_match.group(1)) + len(time_match.group(1)):].strip()

        # Match line
        if ' v ' in line and current_date:
            parts = re.split(r'\s+v\s+', line)
            if len(parts) != 2:
                continue

            home = parts[0].strip()
            away = parts[1].strip()

            cancelled = '[cancelled]' in away
            if cancelled:
                away = away.replace('[cancelled]', '').strip()

            result_match = re.search(r'(\d+-\d+)(?:\s*(pen\.)?(\d+-\d+))?(?:\s*\(\d+-\d+\))?', away)
            if result_match:
                result_str = result_match.group(1)
                penalty_str = result_match.group(3) if result_match.group(3) else None
                away = away[:result_match.start()].strip()
                
                full_time = result_str
                pen_result = penalty_str if penalty_str else None
                aet_result = None

                if 'a.e.t.' in away:
                    aet_result = away.split('a.e.t.')[1].strip()

                result = {"full_time": full_time}
                if aet_result:
                    result["aet"] = aet_result
                if pen_result:
                    result["penalties"] = pen_result
            elif cancelled:
                result = "cancelled"
            else:
                result = None

            match = {
                "date": current_date,
                "time": current_time,
                "home_team": home,
                "away_team": away
            }

            if result:
                match["result"] = result

            if current_matchday:
                current_matchday["matches"].append(match)

    if current_matchday:
        matchdays.append(current_matchday)

    return {
        "league": league,
        "season": season,
        "matchdays": matchdays
    }
