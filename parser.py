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
                if yy <= (start_year % 100):
                    end_year = (century + 1) * 100 + yy
                else:
                    end_year = century * 100 + yy
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
            home_away = re.split(r"\s+v\s+", line)
            if len(home_away) != 2:
                continue
            home, away_part = home_away
            cancelled = '[cancelled]' in away_part
            if cancelled:
                away_part = away_part.replace('[cancelled]', '').strip()

            result = {}

            # Penalties
            pen_match = re.search(r"(\d+-\d+)\s*pen\.", away_part)
            if pen_match:
                result["penalties"] = pen_match.group(1)

            # Extra time
            aet_match = re.search(r"(\d+-\d+)\s*a\.e\.t\.", away_part)
            if aet_match:
                result["extra_time"] = aet_match.group(1)

            # Full time from parentheses
            ft_match = re.search(r"\((\d+-\d+),\s*(\d+-\d+)\)", away_part)
            if ft_match:
                first_half = list(map(int, ft_match.group(1).split('-')))
                second_half = list(map(int, ft_match.group(2).split('-')))
                full_home = first_half[0] + second_half[0]
                full_away = first_half[1] + second_half[1]
                result["full_time"] = f"{full_home}-{full_away}"

            # Clean away team string
            away = re.split(r'\d+-\d+.*', away_part)[0].strip()

            match = {
                "date": current_date,
                "time": current_time,
                "home_team": home.strip(),
                "away_team": away
            }
            if result:
                match["result"] = result
            if cancelled:
                match["cancelled"] = True

            if current_matchday:
                current_matchday["matches"].append(match)

    if current_matchday:
        matchdays.append(current_matchday)

    return {
        "league": league,
        "season": season,
        "matchdays": matchdays
    }
