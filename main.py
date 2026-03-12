import csv
import logging
import os
from fastapi import FastAPI, HTTPException

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)
app = FastAPI()
DATAFILE = os.getenv("DATAFILE", "data.csv")


def load_csv():
    logger.debug(f"DATAFILE: {DATAFILE}")
    if not os.path.exists(DATAFILE):
        logger.error(
            f"Error - can't find file indicated by env variable DATAFILE: {DATAFILE}"
        )
        raise HTTPException(
            status_code=500, detail=f"Internal error: data file is missing"
        )

    with open(DATAFILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


@app.get("/records")
def get_records():
    data = load_csv()
    return data


@app.get("/cities")
def get_cities():
    data = load_csv()
    cities = {row["city"] for row in data}
    return cities


@app.get("/records/age/{min_age}")
def get_records_by_age(min_age: int):
    data = load_csv()
    filtered = [row for row in data if int(row["age"]) >= min_age]
    if not filtered:
        raise HTTPException(
            status_code=404, detail=f"No records found with age above: {min_age}"
        )
    return filtered


@app.get("/records/{city}")
def get_records_by_city(city: str):
    data = load_csv()
    filtered = [row for row in data if row["city"].lower() == city.lower()]
    if not filtered:
        raise HTTPException(
            status_code=404, detail=f"No records found for city: {city}"
        )
    return filtered


@app.get("/summary")
def get_summary():
    data = load_csv()
    total = len(data)
    total_salary = 0
    cities = {}

    for row in data:
        city = row["city"]
        salary = int(row["salary"])
        total_salary += salary
        if city not in cities:
            cities[city] = 0
        cities[city] += 1

    return {
        "total_records": total,
        "average_salary": round(total_salary / total, 2),
        "records_by_city": cities,
    }
