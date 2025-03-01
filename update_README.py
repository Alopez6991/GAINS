import pandas as pd
import os
from datetime import datetime

# File paths
csv_file = "GAINS.csv"
readme_file = "README.md"
stats_dir = "Stats"

def get_latest_date():
    """Reads the CSV file and finds the most recent date."""
    df = pd.read_csv(csv_file)
    df['date'] = pd.to_datetime(df['date'])
    latest_date = df['date'].max().strftime('%Y-%m-%d')
    return latest_date

def get_beast_of_the_day(latest_date):
    """Finds the person with the highest total workout gains."""
    df = pd.read_csv(csv_file)
    
    # Filter for the latest date
    daily_data = df[df['date'] == latest_date]

    # Sum values per person
    total_gains = daily_data.groupby('name')['value'].sum()
    beast_name = total_gains.idxmax()  # Find the person with the highest total

    # Get individual stats for the beast
    beast_stats = daily_data[daily_data['name'] == beast_name].groupby('workout_type')['value'].sum()
    pushups = beast_stats.get('Push-Ups', 0)
    squats = beast_stats.get('Squats', 0)
    situps = beast_stats.get('Sit-Ups', 0)
    total = pushups + squats + situps

    return beast_name, pushups, squats, situps, total

def update_readme(latest_date):
    """Updates the README.md file with the latest images from the Stats directory and the BEAST OF US."""
    
    # Get the Beast of the Day
    beast_name, pushups, squats, situps, total = get_beast_of_the_day(latest_date)

    readme_content = f"""# GAINS Tracker

## 🏆 Today **{beast_name}** is the **BEAST OF US** 🏆  
### {pushups} Push-Ups | {squats} Squats | {situps} Sit-Ups  
**(Total Gains = {total})**

---

## Latest Progress - {latest_date}

### Overall Workout Gains
![Gains]({stats_dir}/gains_{latest_date}.png)

### Lab Workout Statistics
![Stats]({stats_dir}/stats_{latest_date}.png)

### Overall Contribution
![Overall Stats]({stats_dir}/stats_overall_{latest_date}.png)

These graphs are automatically updated daily after each push.
"""

    with open(readme_file, "w") as file:
        file.write(readme_content)

    print(f"README.md updated with images from {latest_date} and BEAST OF US: {beast_name}")

def commit_and_push():
    """Commits and pushes the updated README to GitHub."""
    os.system("git add README.md")
    os.system(f"git commit -m 'Update README with latest stats and BEAST OF US'")
    os.system("git push origin main")

if __name__ == "__main__":
    latest_date = get_latest_date()
    update_readme(latest_date)
    commit_and_push()
