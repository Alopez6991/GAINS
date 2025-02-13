import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime  # Ensure datetime is fully accessible
import os

# File path to the CSV file
csv_file = 'GAINS.csv'

# Directory to save images
stats_dir = 'Stats'
os.makedirs(stats_dir, exist_ok=True)

def get_date():
    today_input = input("Is this for today? (Y/N): ").strip().lower()
    if today_input == 'y':
        return datetime.datetime.today().strftime('%Y-%m-%d')
    else:
        while True:
            date_input = input("Enter the date (YYYY-MM-DD): ").strip()
            try:
                datetime.datetime.strptime(date_input, '%Y-%m-%d')
                return date_input
            except ValueError:
                print("Invalid date format. Please try again.")


def generate_heatmaps(date):
    # Load the data
    data = pd.read_csv(csv_file)

    # Filter data for the given date
    daily_data = data[data['date'] == date]

    if daily_data.empty:
        print(f"No data found for {date}.")
        return

    # Separate data by lab
    n_lab_data = daily_data[daily_data['Lab'] == 'N']
    f_lab_data = daily_data[daily_data['Lab'] == 'F']

    # Organize names with N lab first, then F lab
    sorted_names = list(n_lab_data['name'].unique()) + list(f_lab_data['name'].unique())

    # Ensure workout order is Push-Ups, Squats, Sit-Ups
    workout_order = ['Push-Ups', 'Squats', 'Sit-Ups']

    # Create pivot tables for heatmaps with consistent name and workout ordering
    overall_pivot = daily_data.pivot_table(index='name', columns='workout_type', values='value', aggfunc='sum', fill_value=0).reindex(sorted_names).reindex(columns=workout_order)
    n_lab_pivot = n_lab_data.pivot_table(index='name', columns='workout_type', values='value', aggfunc='sum', fill_value=0).reindex(n_lab_data['name'].unique()).reindex(columns=workout_order)
    f_lab_pivot = f_lab_data.pivot_table(index='name', columns='workout_type', values='value', aggfunc='sum', fill_value=0).reindex(f_lab_data['name'].unique()).reindex(columns=workout_order)

    # Replace NaNs with 0 and convert to integers
    overall_pivot = overall_pivot.fillna(0).astype(int)
    n_lab_pivot = n_lab_pivot.fillna(0).astype(int)
    f_lab_pivot = f_lab_pivot.fillna(0).astype(int)

    # Determine the common color range for lab heatmaps
    vmin = min(n_lab_pivot.min().min(), f_lab_pivot.min().min())
    vmax = max(n_lab_pivot.max().max(), f_lab_pivot.max().max())

    # Plot the heatmaps
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))

    sns.heatmap(overall_pivot, annot=True, cmap='Purples', fmt='d', ax=axes[0])
    axes[0].set_title(f'Overall Workout Gains ({overall_pivot.values.sum()} total)')

    sns.heatmap(n_lab_pivot, annot=True, cmap='Purples', fmt='d', ax=axes[1], vmin=vmin, vmax=vmax)
    axes[1].set_title(f'Nair-o-dynamics Lab Gains ({n_lab_pivot.values.sum()} total)')

    sns.heatmap(f_lab_pivot, annot=True, cmap='Purples', fmt='d', ax=axes[2], vmin=vmin, vmax=vmax)
    axes[2].set_title(f'van Breug-o-nauts Lab Gains ({f_lab_pivot.values.sum()} total)')

    plt.tight_layout()
    plt.savefig(os.path.join(stats_dir,f'gains_{date}.png'))
    plt.close()
    print(f"Heatmaps saved as {stats_dir}/gains_{date}.png")


def format_autopct(pct, allvals):
    total = sum(allvals)
    absolute = int(round(pct / 100. * total))
    return "{:.1f}%\n({:d})".format(pct, absolute)


def generate_stats(date):
    # Load the data
    data = pd.read_csv(csv_file)

    # Filter data for the given date
    daily_data = data[data['date'] == date]

    if daily_data.empty:
        print(f"No data found for {date}.")
        return

    # Separate data by lab
    n_lab_data = daily_data[daily_data['Lab'] == 'N']
    f_lab_data = daily_data[daily_data['Lab'] == 'F']

    # Calculate number of rows needed
    num_rows = 2 + max(len(n_lab_data['name'].unique()), len(f_lab_data['name'].unique()))

    fig, axes = plt.subplots(num_rows, 2, figsize=(14, num_rows * 4))
    fig.suptitle(f'Lab Statistics for {date}', fontsize=16)

    # Assign colors by name for consistency
    n_names = n_lab_data['name'].unique()
    f_names = f_lab_data['name'].unique()
    name_colors = {name: color for name, color in zip(n_names, sns.color_palette("Reds", len(n_names)))}
    name_colors.update({name: color for name, color in zip(f_names, sns.color_palette("Blues", len(f_names)))})

    # First Row: Total gains by workout type for each lab
    n_totals = n_lab_data.groupby('workout_type')['value'].sum()
    f_totals = f_lab_data.groupby('workout_type')['value'].sum()

    axes[0, 0].pie(n_totals, labels=n_totals.index, autopct=lambda pct: format_autopct(pct, n_totals), colors=['#FF9999', '#FF6666', '#FF3333'])
    axes[0, 0].set_title(f'Nair-o-dynamics Total Gains by Workout ({n_totals.sum()} total)')

    axes[0, 1].pie(f_totals, labels=f_totals.index, autopct=lambda pct: format_autopct(pct, f_totals), colors=['#9999FF', '#6666FF', '#3333FF'])
    axes[0, 1].set_title(f'van Breug-o-nauts Total Gains by Workout ({f_totals.sum()} total)')

    # Second Row: Total gains by individual for each lab
    n_individual_totals = n_lab_data.groupby('name')['value'].sum()
    f_individual_totals = f_lab_data.groupby('name')['value'].sum()

    axes[1, 0].pie(n_individual_totals, labels=n_individual_totals.index, autopct=lambda pct: format_autopct(pct, n_individual_totals), colors=[name_colors[name] for name in n_individual_totals.index])
    axes[1, 0].set_title(f'Nair-o-dynamics Total Gains by Person ({n_individual_totals.sum()} total)')

    axes[1, 1].pie(f_individual_totals, labels=f_individual_totals.index, autopct=lambda pct: format_autopct(pct, f_individual_totals), colors=[name_colors[name] for name in f_individual_totals.index])
    axes[1, 1].set_title(f'van Breug-o-nauts Total Gains by Person ({f_individual_totals.sum()} total)')

    # Remaining Rows: Individual breakdowns
    for idx, name in enumerate(n_names):
        individual_data = n_lab_data[n_lab_data['name'] == name].groupby('workout_type')['value'].sum()
        axes[idx + 2, 0].pie(individual_data, labels=individual_data.index, autopct=lambda pct: format_autopct(pct, individual_data), colors=['#FF9999', '#FF6666', '#FF3333'])
        axes[idx + 2, 0].set_title(f'{name} Workout Breakdown ({individual_data.sum()} total)')

    for idx, name in enumerate(f_names):
        individual_data = f_lab_data[f_lab_data['name'] == name].groupby('workout_type')['value'].sum()
        axes[idx + 2, 1].pie(individual_data, labels=individual_data.index, autopct=lambda pct: format_autopct(pct, individual_data), colors=['#9999FF', '#6666FF', '#3333FF'])
        axes[idx + 2, 1].set_title(f'{name} Workout Breakdown ({individual_data.sum()} total)')

    # Last row: Combined contribution from both labs
    combined_totals = daily_data.groupby('name')['value'].sum()

    fig_combined, ax_combined = plt.subplots(figsize=(8, 8))
    ax_combined.pie(combined_totals, labels=combined_totals.index, autopct=lambda pct: format_autopct(pct, combined_totals), colors=[name_colors[name] for name in combined_totals.index])
    ax_combined.set_title(f'Overall Contribution by All Lab Members ({combined_totals.sum()} total)')

    plt.tight_layout()
    fig.savefig(os.path.join(stats_dir,f'stats_{date}.png'))  # Save the main figure with all subplots
    fig_combined.savefig(os.path.join(stats_dir,f'stats_overall_{date}.png'))  # Save the combined contribution chart separately
    plt.close('all')
    print(f"Statistics saved as {stats_dir}/stats_{date}.png \n {stats_dir}/stats_overall_{date}.png")


if __name__ == '__main__':
    date = get_date()
    generate_heatmaps(date)
    generate_stats(date)
    print("Workout statistics generated!")
