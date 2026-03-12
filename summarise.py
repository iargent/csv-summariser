import csv

def load_csv(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        reader=csv.DictReader(f)
        return list(reader)
    
def summarise(data):
    total=len(data)
    cities={}
    total_salary=0
    
    for row in data:
        city = row['city']
        salary=int(row['salary'])
        
        total_salary+=salary
        
        if city not in cities:
            cities[city]=0
        cities[city]+=1
        
    average_salary = total_salary / total
    
    print(f"Total records: {total}")
    print(f"Average salary: {average_salary:.2f}")
    print(f"\n Records by city:")
    for city, count in cities.items():
        print(f"  {city}: {count}")
        
data = load_csv('data.csv')
summarise(data)
