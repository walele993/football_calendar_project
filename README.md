# ⚽ Football Calendar Project

*Automate football match data extraction and conversion for various leagues!*

---

## 🚀 Introduction

**Football Calendar Project** is a Python-based backend tool that extracts football match data from textual sources provided by openfootball and converts them into a structured JSON format. It automates the extraction process by reading the TXT files (Football.TXT format) from openfootball, parses them into a detailed match calendar, and outputs JSON files organized by league and season. These JSON files offer a clean, easy-to-use football match calendar, ready for integration into various applications and further analysis.

### Key Features
- 🏆 **Matchday & Round Organization**: Automatically organizes match data by league, season, matchday, and rounds.
- 📅 **Detailed Fixtures**: Supports multiple leagues and seasons, capturing match dates, times, teams, and results.
- 🔄 **Data Conversion**: Converts publicly available TXT files from openfootball into structured JSON format.
- 🗂️ **Easy Integration**: JSON output is standardized and ready for use in web or mobile applications for football scheduling and analysis.

---

## 🛋️ Installation

### Prerequisites
- Python 3.x
- Requests
- JSON (built into Python)

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 💻 Usage

1. **Convert TXT Files to JSON**  
   Run the conversion script to extract and convert match data from TXT files into JSON. The TXT files are sourced from openfootball repositories.
   ```bash
   python converter.py --input_folder ./openfootball_txt --output_folder ./parsed_json
   ```
   - **Input Folder**: Folder containing the TXT files (downloaded from openfootball).
   - **Output Folder**: Folder where the corresponding JSON files will be generated. Each TXT file is converted into a JSON file named using the league and season (e.g., `(2024/25) UEFA Europa League.json`).

2. **Review Output**  
   The output JSON files in the `parsed_json` folder contain structured match data with the following information:
   - **League**: Name of the football league (e.g., Italian Serie A, UEFA Champions League).
   - **Season**: The season year (e.g., 2023/24).
   - **Matchdays**: An array of matchdays or rounds, each containing a list of matches.
   - **Matches**: Each match includes the date, time, home team, away team, and result details (full-time score, half-time score, penalties, etc.).

---

## 🧠 Data Structure

The JSON output is structured as follows:

```json
{
  "league": "Italian Serie A",
  "season": "2023/24",
  "matchdays": [
    {
      "matchday": "Matchday 1",
      "matches": [
        {
          "date": "2024-08-11",
          "time": "20:00",
          "home_team": "ACF Fiorentina",
          "away_team": "Torino FC",
          "result": {
            "full_time": "1-0"
          }
        },
        ...
      ]
    },
    ...
  ]
}
```

*Note: The exact field names can vary based on the details available in the TXT files.*

---

## 📝 Key Functions

### Data Extraction & Processing
- **`parse_football_txt(content)`**  
  Parses match data from an input TXT file (Football.TXT format) and structures it into JSON with league, season, and matchdays.

- **`convert_folder(input_folder, output_folder)`**  
  Recursively processes all TXT files in a given folder, converts them into JSON files (each named with league and season), and saves them in an output folder.

### Output
- **JSON Files**: Each TXT file from openfootball is converted into an individual JSON file stored in the `parsed_json` folder, named in the format `(season) league.json` to avoid overwriting duplicates.

---

## 💪 Future Enhancements

- 🌍 Expand support for additional leagues.
- 📅 Enhance calendar functionalities with automated scheduling and reminders.
- 📝 Incorporate detailed match analysis and performance metrics.

---

## 🏅 Contribution

This is a **work-in-progress** project, and I welcome your feedback!  

1. **Fork** the repository  
2. **Clone** your fork:  
   ```bash
   git clone https://github.com/your-username/football-calendar-project.git
   ```
3. Create a **feature branch**:  
   ```bash
   git checkout -b feature-enhancement
   ```
4. **Push** your changes and submit a **pull request**

---

## 🏁 Credits

Project created by **Gabriele Meucci**.  
Data is sourced from publicly available football fixtures in the Football.TXT format provided by openfootball.

---

*Ready to organize and analyze football match data like never before? Let's go!* ⚽🔥
