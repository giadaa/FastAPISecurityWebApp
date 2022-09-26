# import json
# from fastapi import status
# def test_create_dependency(client, normal_user_token_headers):
#     data = {
#         "name": "dependency",
#         "latest_version": "doogle",
#         "deadline": "2022-03-21",
#         "date_posted": "2022-03-20",
#     }
#     response = client.post(
#         "/dependencies/create-dependency/",
#         json.dumps(data),
#         headers=normal_user_token_headers,
#     )
#     assert response.status_code == 200
#     assert response.json()["latest_version"] == "doogle"
# def test_read_dependency(client, normal_user_token_headers):
#     data = {
#         "name": "dependency",
#         "latest_version": "doogle",
#         "deadline": "2022-03-21",
#         "date_posted": "2022-03-20",
#     }
#     response = client.post(
#         "/dependencies/create-dependency/",
#         json.dumps(data),
#         headers=normal_user_token_headers,
#     )
#     response = client.get("/dependencies/get/1/")
#     assert response.status_code == 200
#     assert response.json()["name"] == "dependency"
# def test_read_all_dependencies(client, normal_user_token_headers):
#     data = {
#         "name": "dependency",
#         "latest_version": "doogle",
#         "deadline": "2022-03-21",
#         "date_posted": "2022-03-20",
#     }
#     client.post(
#         "/dependencies/create-dependency/",
#         json.dumps(data),
#         headers=normal_user_token_headers,
#     )
#     client.post(
#         "/dependencies/create-dependency/",
#         json.dumps(data),
#         headers=normal_user_token_headers,
#     )
#     response = client.get("/dependencies/all/")
#     assert response.status_code == 200
#     assert response.json()[0]
#     assert response.json()[1]
# def test_update_a_dependency(client, normal_user_token_headers):
#     data = {
#         "name": "dependency",
#         "latest_version": "doogle",
#         "deadline": "2022-03-21",
#         "date_posted": "2022-03-20",
#     }
#     client.post(
#         "/dependencies/create-dependency/",
#         json.dumps(data),
#         headers=normal_user_token_headers,
#     )
#     data["name"] = "test new dependency name"
#     response = client.post(
#         "/dependencies/update/1", json.dumps(data), headers=normal_user_token_headers
#     )
#     assert response.json()["msg"] == "Successfully updated data."
#     response = client.get("/dependencies/get/1/")
#     assert response.json()["name"] == data["name"]
# def test_delete_a_dependency(client, normal_user_token_headers):
#     data = {
#         "name": "dependency",
#         "latest_version": "doogle",
#         "deadline": "2022-03-21",
#         "date_posted": "2022-03-20",
#     }
#     client.post(
#         "/dependencies/create-dependency/",
#         json.dumps(data),
#         headers=normal_user_token_headers,
#     )
#     client.delete("/dependencies/delete/1", headers=normal_user_token_headers)
#     response = client.get("/dependencies/get/1/")
#     assert response.status_code == status.HTTP_404_NOT_FOUND
