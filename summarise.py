import csv
import os
import sys


def load_csv(filename):
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def summarise(data):
    total = len(data)
    cities = {}
    total_salary = 0

    for row in data:
        city = row["city"]
        salary = int(row["salary"])

        total_salary += salary

        if city not in cities:
            cities[city] = 0
        cities[city] += 1

    average_salary = total_salary / total

    print(f"Total records: {total}")
    print(f"Average salary: {average_salary:.2f}")
    print(f"\nRecords by city:")
    for city, count in cities.items():
        print(f"  {city}: {count}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        datafile = sys.argv[1]
        if not os.path.exists(datafile):
            print(f"Error - Can't find file: {datafile}", file=sys.stderr)
            raise SystemExit(1)
    else:
        datafile = "data.csv"

    data = load_csv(datafile)
    summarise(data)
