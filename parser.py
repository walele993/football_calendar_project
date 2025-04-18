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
            # Detect season string like '2024/25'
            season_match = re.search(r"(\d{4})/(\d{2})$", title_line)
            if season_match:
                # Extract start and end years
                start_year = int(season_match.group(1))
                yy = int(season_match.group(2))
                century = start_year // 100
                # compute end year
                if yy < (start_year % 100):
                    end_year = century * 100 + yy
                else:
                    end_year = (century + 1) * 100 + yy
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
            current_matchday = {
                "matchday": line.lstrip('» ').strip(),
                "matches": []
            }
            continue

        # Date line, capture month/day and optional year
        date_match = re.match(r"(?:[A-Za-z]{3}\s+)?([A-Za-z]{3})/(\d{1,2})(?:\s+(\d{4}))?", line)
        if date_match:
            mon_str, day_str, year_str = date_match.groups()
            month = datetime.strptime(mon_str, '%b').month
            day = int(day_str)
            # Record season_start_month on first date
            if season_start_month is None:
                season_start_month = month
                # If no season header, initialize year from first explicit date
                if not cross_year and year_str:
                    season_start_year = int(year_str)

            # Determine year for this date
            if year_str:
                year = int(year_str)
            else:
                if cross_year:
                    # rollover: months before start month are next calendar year
                    if month >= season_start_month:
                        year = season_start_year
                    else:
                        year = season_end_year
                else:
                    year = season_start_year

            current_date = f"{year:04d}-{month:02d}-{day:02d}"
            continue

        # Time line
        time_match = re.match(r"(\d{1,2}\.\d{2})", line)
        if time_match:
            current_time = time_match.group(1).replace('.', ':')
            # remove time from line to isolate teams
            line = line[time_match.end():].strip()

        # Match line
        if ' v ' in line and current_date:
            home_away = re.split(r"\s+v\s+", line)
            if len(home_away) != 2:
                continue
            home, away_part = home_away
            cancelled = '[cancelled]' in away_part
            if cancelled:
                away_part = away_part.replace('[cancelled]', '').strip()

            # Extract results
            result = None
            res_match = re.search(r"(\d+-\d+)(?:\s*(pen\.)?(\d+-\d+))?", away_part)
            if res_match:
                ft = res_match.group(1)
                pen = res_match.group(3)
                result = {"full_time": ft}
                if pen:
                    result["penalties"] = pen
                # strip result from away team
                away = away_part[:res_match.start()].strip()
            else:
                away = away_part
                if cancelled:
                    result = 'cancelled'

            match = {
                "date": current_date,
                "time": current_time,
                "home_team": home.strip(),
                "away_team": away
            }
            if result:
                match["result"] = result
            if current_matchday:
                current_matchday["matches"].append(match)

    # append last matchday
    if current_matchday:
        matchdays.append(current_matchday)

    return {
        "league": league,
        "season": season,
        "matchdays": matchdays
    }
