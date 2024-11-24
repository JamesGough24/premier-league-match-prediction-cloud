import csv

def save_data_to_csv(data, filename="match_data.csv"):
    keys = data[0].keys

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)