import csv
from pathlib import Path

def save_to_csv(stats, filepath='results.csv'):
    file = Path(filepath)
    write_header = not file.exists()

    with open(file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=stats.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(stats)
