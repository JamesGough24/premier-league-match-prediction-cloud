import csv
from io import StringIO

def save_data_to_csv(data, filename="match_data.csv"):
    # Get the keys from the first match to set as CSV headers 
    keys = data[0].keys

    # Create an in-memory buffer
    csv_buffer = StringIO()

    # Write the CSV to the buffer
    writer = csv.DictWriter(csv_buffer, fieldnames=keys)
    writer.writeheader()
    writer.writerows(data)

    # Reset the buffer's back to the start 
    csv_buffer.seek(0)

    return csv_buffer
    