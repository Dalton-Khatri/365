import csv
import json
def read_csv(filename, data):
    with open(filename,'r') as csv_file:
        reader=csv.DictReader(csv_file)
        for row in reader:
            data.append(row)
    return data

def write_json(data, filename):
    with open(filename,'w') as json_file:
        json.dump(data,json_file,indent=4)

def convert_csv_to_json(csv_file, json_file):
    data = []
    data = read_csv(csv_file, data)
    write_json(data, json_file)

if __name__ == "__main__":
    csv_file = 'students.csv'
    json_file = 'result.json'
    convert_csv_to_json(csv_file, json_file)