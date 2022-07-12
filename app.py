"""
This module contains example code for Flask usage.
Feel free to modify this file in any way.
"""
import json

from auth import introspect_token
from db import get_num_projects, initialize_db, create_project, read_project, delete_project, comment_project
from flask import Flask, Response, request, jsonify, make_response
from functools import wraps


app = Flask(__name__)
initialize_db()

# token decorator 
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # pass jwt-token in headers
        if 'authorization' in request.headers:
            token = request.headers['authorization']
        if not token: # throw error if no token provided
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
            access_token = token[len("Bearer ") :]
            token_info = introspect_token(access_token)
            user_info = token_info["user_info"]
        except:
            return make_response(jsonify({"message": "Invalid token!"}), 401)

        return f(user_info, *args, **kwargs)
    return decorator

@app.route("/", methods=["GET"])
@token_required
def example(user_info):
    """
    Basic example of GET to / using Flask
    Does not handle missing or invalid Access Tokens
    """
    if request.method == "GET":
        # get bearer token from auth header
        # auth_header = request.headers.get("authorization")
        # access_token = auth_header[len("Bearer ") :]

        # get username and num_projects to respond with
        # token_info = introspect_token(access_token)
        # user_info = token_info["user_info"]
        username = user_info["username"] #user_info["username"]
        num_projects = get_num_projects()

        # respond
        response_dict = {
            "message": (
                "Hello {}, there are {} projects in the database!".format(
                    username, num_projects
                )
            )
        }
        return make_response(jsonify(response_dict), 200)
    return make_response(jsonify({"message": "Not Allowed"}), 403)

@app.route("/projects/<project_id>", methods=["GET"])
@token_required
def get_project(user_info, project_id):
    '''get a project by <project_id>'''
    p = read_project(project_id)
    print(p)
    if p is not None:
        return make_response(jsonify(p))
    return make_response(jsonify({"message": "Not Found"}), 404)


@app.route("/projects", methods=["POST"])
@token_required
def add_project(user_info):
    '''adds a new project'''
    data = request.get_json()
    if data["project_name"] == "":
        return make_response(jsonify({"message": "Project name is required!"}), 400)
    else:
        data["owner_id"] = user_info["user_id"]
        data["owner_username"] = user_info["username"]
        new_project = create_project(data)
        return make_response(jsonify(new_project))

@app.route("/projects/<project_id>", methods=["DELETE"])
@token_required
def remove_project(user_info, project_id):
    '''delete a project by <project_id>'''
    p = delete_project(project_id)
    if p is not None:
        return make_response(jsonify(p))
    return make_response(jsonify({"message": "Not Found"}), 404)


@app.route("/projects/<project_id>/comments", methods=["POST"])
@token_required
def comments_project(user_info, project_id):
    '''comment a project by <project_id>'''
    data = request.get_json()
    comment = dict(commenter_id=user_info["user_id"], commenter_username=user_info["username"], message=data["message"])
    p = comment_project(project_id, comment)
    if p is not None:
        return make_response(jsonify(p))
    return make_response(jsonify({"message": "Not Found"}), 404)



if __name__ == "__main__":
    app.run()
