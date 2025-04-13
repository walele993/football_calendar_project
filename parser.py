import re
from datetime import datetime

def parse_football_txt(content):
    competition = None
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

        # Competition title (handling both formats)
        if line.startswith('= '):
            # Check if it contains both the league and season (e.g., "English Premier League 2023/24")
            parts = line[2:].strip().split(' ', 1)
            if len(parts) > 1 and re.match(r'\d{4}/\d{2}', parts[1]):
                # It's a league with season format (e.g., "English Premier League 2023/24")
                competition = parts[0]
                season = parts[1]
            else:
                # It could be a competition name without the year (e.g., "FA Cup")
                competition = line[2:].strip()
            continue

        # Matchday or round
        matchday_match = re.match(r'» (Matchday \d+|[A-Za-z ]+Round|Quarterfinals|Semifinals|Final)', line)
        if matchday_match:
            if current_matchday:
                matchdays.append(current_matchday)
            current_matchday = {
                "matchday": matchday_match.group(1),
                "matches": []
            }
            continue

        # Date
        date_match = re.match(r'([A-Za-z]{3} [A-Za-z]{3}/\d{2}(?: \d{4})?)', line)
        if date_match:
            try:
                parts = date_match.group(1).split(' ', 1)[1]
                if len(parts.split()[-1]) == 4:
                    current_date = datetime.strptime(parts, '%b/%d %Y').strftime('%Y-%m-%d')
                else:
                    # Add dummy year if missing
                    current_date = datetime.strptime(parts + ' 2024', '%b/%d %Y').strftime('%Y-%m-%d')
            except:
                current_date = None
            continue

        # Time
        time_match = re.match(r'(\d{1,2}\.\d{2})', line)
        if time_match:
            current_time = time_match.group(1).replace('.', ':')
            line = line[line.find(time_match.group(1)) + len(time_match.group(1)):].strip()

        # Match
        if ' v ' in line and current_date:
            parts = re.split(r'\s+v\s+', line)
            if len(parts) != 2:
                continue

            home = parts[0].strip()
            away = parts[1].strip()

            cancelled = '[cancelled]' in away
            if cancelled:
                away = away.replace('[cancelled]', '').strip()

            # Score (optional)
            result_match = re.search(r'(\d+-\d+)(?:\s*(pen\.)?(\d+-\d+))?(?:\s*\(\d+-\d+\))?', away)
            if result_match:
                result_str = result_match.group(1)
                penalty_str = result_match.group(3) if result_match.group(3) else None
                away = away[:result_match.start()].strip()
                
                full_time = result_str
                halftime = None
                
                # Handle penalties and extra time (a.e.t.)
                pen_result = penalty_str if penalty_str else None
                aet_result = None

                # Check for a.e.t.
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
        "league": competition,
        "season": season,
        "matchdays": matchdays
    }