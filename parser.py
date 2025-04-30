import re
from datetime import datetime

def parse_football_txt(content):
    league = None
    season = None
    matchdays = []
    current_matchday = None
    current_date = None
    current_time = None

    # Season rollover variables
    season_start_year = None
    season_end_year = None
    season_start_month = None
    cross_year = False

    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Parse league and season header
        if line.startswith('= '):
            title_line = line[2:].strip()
            season_match = re.search(r"(\d{4})/(\d{2})$", title_line)
            if season_match:
                start_year = int(season_match.group(1))
                yy = int(season_match.group(2))
                century = start_year // 100
                end_year = ((century + 1) * 100 + yy) if yy <= (start_year % 100) else (century * 100 + yy)
                season_start_year = start_year
                season_end_year = end_year
                cross_year = True
                season = season_match.group(0)
                league = title_line[:season_match.start()].strip()
            else:
                league = title_line
                season = None
            continue

        # Matchday marker
        if line.startswith('»') or re.match(r'(Matchday \d+|[A-Za-z ]+Round \d+|Finals?)', line):
            if current_matchday:
                matchdays.append(current_matchday)
            current_matchday = {"matchday": line.lstrip('» ').strip(), "matches": []}
            continue

        # Date line
        date_match = re.match(r"(?:[A-Za-z]{3}\s+)?([A-Za-z]{3})/(\d{1,2})(?:\s+(\d{4}))?", line)
        if date_match:
            mon_str, day_str, year_str = date_match.groups()
            month = datetime.strptime(mon_str, '%b').month
            day = int(day_str)
            if season_start_month is None:
                season_start_month = month
                if not cross_year and year_str:
                    season_start_year = int(year_str)
            if year_str:
                year = int(year_str)
            else:
                if cross_year:
                    year = season_start_year if month >= season_start_month else season_end_year
                else:
                    year = season_start_year
            current_date = f"{year:04d}-{month:02d}-{day:02d}"
            continue

        # Time line
        time_match = re.match(r"(\d{1,2}\.\d{2})", line)
        if time_match:
            current_time = time_match.group(1).replace('.', ':')
            line = line[time_match.end():].strip()

        # Match line
        if ' v ' in line and current_date:
            home, away_part = re.split(r"\s+v\s+", line)
            cancelled = '[cancelled]' in away_part
            if cancelled:
                away_part = away_part.replace('[cancelled]', '').strip()

            result = {}
            # handle cases with a.e.t. and penalties
            if re.search(r"a\.?e\.?t\.?") and 'pen' in away_part:
                paren = re.search(r"\((\d+-\d+),", away_part)
                if paren:
                    result['full_time'] = paren.group(1)
                aet = re.search(r"a\.?e\.?t\.?\s*(\d+-\d+)", away_part)
                if aet:
                    result['after_extra_time'] = aet.group(1)
                pen = re.search(r"(\d+-\d+)\s*pen", away_part)
                if pen:
                    result['penalties'] = pen.group(1)
                away = re.split(r"\s*\d+-\d+", away_part)[0].strip()
            else:
                res_match = re.search(r"(\d+-\d+)", away_part)
                if res_match:
                    result['full_time'] = res_match.group(1)
                    away = away_part[:res_match.start()].strip()
                else:
                    away = away_part

            match = {
                "date": current_date,
                "time": current_time,
                "home_team": home.strip(),
                "away_team": away.strip()
            }
            if result:
                match["result"] = result
            if current_matchday:
                current_matchday["matches"].append(match)

    if current_matchday:
        matchdays.append(current_matchday)

    return {"league": league, "season": season, "matchdays": matchdays}
