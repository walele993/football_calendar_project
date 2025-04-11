# ⚽ Football Calendar Project

*Automate football match data extraction and visualization for various leagues!*  

---

## 🚀 Introduction

**Football Calendar Project** is a Python-based tool that extracts and processes football match data for various leagues. This project organizes matches by matchdays, tracks results, and outputs them in a clean JSON format. Designed to work with multiple leagues, this tool aims to assist in football scheduling and analysis.

### Key Features
- 🏆 **Matchday Organization**: Automatically organizes match results by competition and season.
- 📅 **Comprehensive Calendar**: Supports multiple leagues and seasons, handling matchups, times, and results.
- 🔄 **Automatic Data Extraction**: Scrapes match data and generates structured JSON files for further use.
- 🗂️ **Easy to Integrate**: Output is in JSON format, ready for integration into various applications or services.

---

## 🛋️ Installation

### Prerequisites
- Python 3.x
- Requests
- BeautifulSoup4 (for web scraping)
- JSON

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 💻 Usage

1. **Convert Data to JSON**:  
   Run the conversion script to extract and convert match data into JSON format:
   ```bash
   python converter.py
   ```

2. **View Match Data**:  
   The output JSON files will be saved in the `json_output` directory. Each file contains structured match data for different competitions.

3. **Process Multiple Files**:  
   If you have multiple league files, use the recursive feature to convert all match files at once:
   ```bash
   python converter.py --process_all
   ```

4. **Customize Source Folder**:  
   If you wish to specify a custom folder containing your football text files:
   ```bash
   python converter.py --input_folder ./custom_folder
   ```

---

## 🧠 Data Structure

The JSON files will be structured as follows:

```json
{
  "competition": "English Premier League",
  "season": "2023/24",
  "matchdays": [
    {
      "matchday": 1,
      "matches": [
        {
          "date": "2024-08-11",
          "time": "20:00",
          "home_team": "Burnley FC",
          "away_team": "Manchester City FC",
          "result": {
            "full_time": "0-3",
            "half_time": "0-2"
          }
        },
        ...
      ]
    },
    ...
  ]
}
```

Where:
- **competition**: Name of the football league.
- **season**: The season year (e.g., 2023/24).
- **matchday**: Matchday number or name.
- **matches**: List of match details, including date, time, teams, and results.

---

## 📝 Key Functions

### ✨ Data Extraction & Processing
- **`parse_football_txt(content)`** → Parses match data from text content and structures it into a JSON format.
- **`convert_folder(input_root, output_root)`** → Processes all `.txt` files in a folder structure, converting them into JSON.

### 📊 Data Visualization & Analysis
- Currently, this project focuses on extracting match data and structuring it. Future enhancements will include:
  - Generating match summaries and analysis.
  - Visualizing team performance and rankings.

---

## 💪 Future Enhancements

- 🌍 Expand support for more football leagues (e.g., Serie A, La Liga, Bundesliga).
- 📅 Add calendar features for automated match reminders and scheduling.
- 📝 Include additional match analysis (e.g., win rates, team performance).

---

## 🏅 Contribution

This is a **work-in-progress** project, and I would love your feedback!  

1. **Fork** the repository  
2. **Clone** your fork:  
   ```bash
   git clone https://github.com/your-username/football-calendar.git
   ```
3. Create a **feature branch**:  
   ```bash
   git checkout -b feature-enhancement
   ```
4. **Push** changes & submit a **pull request**

---

## 🏁 Credits

Project created by **Gabriele Meucci**.  

Data sourced from football fixtures (usually parsed from textual formats, such as those found on sports websites).

---

*Ready to organize and analyze football like never before? Let’s go!* ⚽🔥