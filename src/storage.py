import csv
import os

FILE_PATH = "data/transactions.csv"

def save_transactions(transactions):
    file_exists = os.path.isfile(FILE_PATH)

    with open(FILE_PATH, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=transactions[0].keys())

        if not file_exists:
            writer.writeheader()

        for tx in transactions:
            writer.writerow(tx)
