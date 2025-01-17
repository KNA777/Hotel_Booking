import json

# Исходный словарь
data = {
    "name": "ivan",
    "age": 30,
    "city": "moscow"
}

# Преобразование словаря в JSON
json_data = json.dumps(data)

print(json_data)