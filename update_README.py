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

def update_readme(latest_date):
    """Updates the README.md file with the latest images from the Stats directory."""
    readme_content = f"""# GAINS Tracker

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

    print(f"README.md updated with images from {latest_date}")

def commit_and_push():
    """Commits and pushes the updated README to GitHub."""
    os.system("git add README.md")
    os.system(f"git commit -m 'Update README with latest stats'")
    os.system("git push origin main")

if __name__ == "__main__":
    latest_date = get_latest_date()
    update_readme(latest_date)
    commit_and_push()
