"""
This module contains an example of a requests based test for the example app.
Feel free to modify this file in any way.
"""
from email import header
import json
import requests

# testing constants that match values in auth.py
BASE_URL = "http://127.0.0.1:5000"
ACCESS_TOKEN_1 = "31cd894de101a0e31ec4aa46503e59c8"
ACCESS_TOKEN_2 = "97778661dab9584190ecec11bf77593e"
USERNAME_1 = "challengeuser1"
USERNAME_2 = "challengeuser2"
USER_ID_1 = "8bde3e84-a964-479c-9c7b-4d7991717a1b"
USER_ID_2 = "45e3c49a-c699-405b-a8b2-f5407bb1a133"


# def example_test():
#     """
#     Example of using requests to make a test call to the example Flask app
#     """
#     path = BASE_URL + "/"

#     for access_token, username in [
#         (ACCESS_TOKEN_1, USERNAME_1),
#         (ACCESS_TOKEN_2, USERNAME_2),
#     ]:
#         headers = {
#             "Accept": "application/json",
#             "Content-Type": "application/json",
#             "Authorization": "Bearer " + access_token,
#         }

#         r = requests.get(path, headers=headers)
#         message = r.json()["message"]
#         assert "Hello {}".format(username) in message
#         assert "0 projects" in message


def create_test():
    """
    test create api
    """
    path = BASE_URL + "/projects"

    for access_token, username in [
        (ACCESS_TOKEN_1, USERNAME_1),
        (ACCESS_TOKEN_2, USERNAME_2),
    ]:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token,
        }
        data = json.dumps({"project_name": "New Project"})
        r = requests.post(url=path, data=data, headers=headers)
        assert r.ok
        message = r.json()["project_name"]
        assert "New Project" in message


def get_test():
    """
    test get api
    """

    for access_token, username in [
        (ACCESS_TOKEN_1, USERNAME_1),
        (ACCESS_TOKEN_2, USERNAME_2),
    ]:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token,
        }
        data = json.dumps({"project_name": "New Project"})
        path = BASE_URL + "/projects"
        r = requests.post(url=path, data=data, headers=headers)
        assert r.ok
        project_id = r.json()["project_id"]
        path = path + "/" + project_id
        r = requests.get(url=path, headers=headers)
        assert r.ok
        p_name = r.json()["project_name"]
        p_id = r.json()["project_id"]
        assert "New Project" in p_name
        assert project_id in p_id


def delete_test():
    """
    test delete api
    """

    for access_token, username in [
        (ACCESS_TOKEN_1, USERNAME_1),
        (ACCESS_TOKEN_2, USERNAME_2),
    ]:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token,
        }
        data = json.dumps({"project_name": "New Project"})
        path = BASE_URL + "/projects"
        r = requests.post(url=path, data=data, headers=headers)
        assert r.ok
        project_id = r.json()["project_id"]
        path = path + "/" + project_id
        r = requests.get(url=path, headers=headers)
        assert r.ok
        row = r.json()
        p_id = row["project_id"]
        path = BASE_URL + "/projects/" + p_id
        r = requests.delete(url=path, headers=headers)
        assert r.ok
        row = r.json()
        pd_id = row["project_id"]
        assert pd_id in p_id


def comment_test():
    """
    test comment api
    """

    for access_token, username in [
        (ACCESS_TOKEN_1, USERNAME_1),
        (ACCESS_TOKEN_2, USERNAME_2),
    ]:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token,
        }
        data = json.dumps({"project_name": "New Project"})
        path = BASE_URL + "/projects"
        r = requests.post(url=path, data=data, headers=headers)
        project_id = r.json()["project_id"]
        path = path + "/" + project_id
        r = requests.get(url=path, headers=headers)
        row = r.json()
        p_id = row["project_id"]
        path = BASE_URL + "/projects/" + p_id + "/comments"
        data = json.dumps({"message": "Sample Message"})
        r = requests.post(url=path, data=data, headers=headers)
        assert r.ok
        row = r.json()
        msg = row["message"]
        assert "Sample Message" in msg


if __name__ == "__main__":
    create_test()
    get_test()
    delete_test()
    comment_test()
