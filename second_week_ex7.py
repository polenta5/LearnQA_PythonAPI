import requests

response_without_method = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"Запрос без указания метода возвращает: {response_without_method.text}")

response_out_ex_list = requests.patch("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"Запрос не из списка к заданию возвращает код ошибки: {response_out_ex_list.status_code}")

response_with_right_method = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type",
                                           data={"method": "POST"})
print(f"Запрос с правильным значением method возвращает: {response_with_right_method.text}")

print("===============================")

method_list = [{"method": "GET"}, {"method": "POST"}, {"method": "PUT"}, {"method": "DELETE"}]
for meth in method_list:
    response_get = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=meth)
    print(f"На запрос GET cо значением method={meth.get('method')} возвращается: {response_get.text}")
    if meth.get('method') != "GET" and response_get.text == '{"success":"!"}':
        print("ATTENTION!")

print("===============================")

for meth in method_list:
    response_post = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=meth)
    print(f"На запрос POST cо значением method={meth.get('method')} возвращается: {response_post.text}")
    if meth.get('method') != "POST" and response_post.text == '{"success":"!"}':
        print("ATTENTION!")

print("===============================")

for meth in method_list:
    response_put = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=meth)
    print(f"На запрос PUT cо значением method={meth.get('method')} возвращается: {response_put.text}")
    if meth.get('method') != "PUT" and response_put.text == '{"success":"!"}':
        print("ATTENTION!")

print("===============================")

for meth in method_list:
    response_delete = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=meth)
    print(f"На запрос DELETE cо значением method={meth.get('method')} возвращается: {response_delete.text}")
    if meth.get('method') != "DELETE" and response_delete.text == '{"success":"!"}':
        print("ATTENTION!")
