import csv
from datetime import datetime

# File path to the CSV file
csv_file = 'GAINS.csv'

def get_date():
    today_input = input("Is this for today? (Y/N): ").strip().lower()
    if today_input == 'y':
        return datetime.today().strftime('%Y-%m-%d')
    else:
        while True:
            date_input = input("Enter the date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(date_input, '%Y-%m-%d')
                return date_input
            except ValueError:
                print("Invalid date format. Please try again.")

def get_integer(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter a valid integer.")


def add_workout_entry():
    date = get_date()

    # Load existing data to check for duplicates and lab assignments
    existing_entries = set()
    name_lab_map = {}
    try:
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) < 5:
                    continue  # Skip incomplete rows
                existing_entries.add((row[0], row[1], row[3]))  # date, name, workout_type
                if row[1] not in name_lab_map:
                    name_lab_map[row[1]] = row[2]  # name -> Lab
    except FileNotFoundError:
        pass  # If file doesn't exist, proceed without error

    while True:
        name = input("Who is this for? (Type 'exit' to finish): ").strip()
        if name.lower() == 'exit':
            break

        if name in name_lab_map:
            lab = name_lab_map[name]
        else:
            lab_input = input("Nair-o-dynamics? or van Breug-o-nauts? (N/F): ").strip().upper()
            while lab_input not in ['N', 'F']:
                lab_input = input("Please enter 'N' for Nair-o-dynamics or 'F' for van Breug-o-nauts: ").strip().upper()
            lab = lab_input
            name_lab_map[name] = lab

        push_ups = get_integer("What are their push-up gains? ")
        squats = get_integer("What are their squat gains? ")
        sit_ups = get_integer("What are their sit-up gains? ")

        # Check for duplicate entries before adding
        new_entries = [
            (date, name, lab, 'Push-Ups', push_ups),
            (date, name, lab, 'Squats', squats),
            (date, name, lab, 'Sit-Ups', sit_ups)
        ]

        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            for entry in new_entries:
                if (entry[0], entry[1], entry[3]) not in existing_entries:
                    writer.writerow(entry)
                    existing_entries.add((entry[0], entry[1], entry[3]))
                    print(f"Added {entry[3]} data for {name} in Lab {lab} on {date}.")
                else:
                    print(f"Entry for {entry[3]} for {name} on {date} already exists. Skipping.")

if __name__ == '__main__':
    add_workout_entry()
    print("Workout data entry completed!")

