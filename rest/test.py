import requests

BASE = "http://127.0.0.1:5000/"

data = [{"fio": 'Karl'},
		{"fio": 'John'},
		{"fio": 'Mike'}]

for i in range(len(data)):
	response = requests.put(BASE + "user/" + str(i), data[i]) 
	print(response.json())

input('first_get')
response = requests.get(BASE + "user/2")
print(response.json())

input('patch')
response = requests.patch(BASE + "user/1", {"fio": 'Raphael'})
print(response.json())


input('second_get')
response = requests.get(BASE + "user/2")
print(response.json())

input('delete')
resource = requests.delete(BASE + "user/2")
print(response.json())