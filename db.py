"""
This module contains example code for basic SQLite usage.
Feel free to modify this file in any way.
"""
from asyncio.windows_events import NULL
import sqlite3
import uuid

import json

from flask import jsonify

# on import create or connect to an existing db
# and turn on foreign key constraints
conn = sqlite3.connect("globus_challenge.db", check_same_thread=False)
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON;")
conn.commit()


def initialize_db():
    """
    Creates tables in the database if they do not already exist.
    Make sure to clean up old .db files on schema changes.
    """
    try:
        c.execute(
            """
           CREATE TABLE "projects" (
                "project_id" TEXT,
                "owner_id" text,
                "owner_username" TEXT,
                "project_name" TEXT,
                "comments" TEXT,
                PRIMARY KEY ("project_id")
            );
            """
        )
        conn.commit()
    except sqlite3.OperationalError:
        pass


def get_num_projects():
    """
    Count project records
    """
    c.execute("SELECT COUNT(project_id) FROM projects")
    return c.fetchone()[0]


def create_project(data):
    """
    Create new project record
    """
    project_id = str(uuid.uuid4())
    c.execute('INSERT INTO projects (project_id, owner_id, owner_username, project_name, comments) values (?,?,?,?,?)',
              [
                  project_id,
                  data["owner_id"],
                  data["owner_username"],
                  data["project_name"],
                  json.dumps([])
              ]
              )
    conn.commit()
    return read_project(project_id)


def read_project(id):
    """
    Get a project record by id
    """

    c.execute("SELECT * FROM projects WHERE project_id = ?", [id])
    row = c.fetchone()
    if row is not None:
        proj = dict(project_id=row[0], owner_id=row[1], owner_username=row[2],
                    project_name=row[3], comments=(json.loads(row[4])))
        return proj
    else:
        return row


def delete_project(id):
    """
    Delete a project record by id
    """
    row = read_project(id)
    print(row)
    if row is not None:
        c.execute("DELETE FROM projects WHERE project_id = ?", [id])
        conn.commit()
        return row
    else:
        return None


def comment_project(project_id, data):
    """
    Comment a project by project_id
    """
    data["comment_id"] = str(uuid.uuid4())
    row = read_project(project_id)
    if row is not None:
        comments = row["comments"]
        comments.append(data)
        comments = json.dumps(comments).replace("\'", "\"")

        c.execute("UPDATE projects SET comments = ? WHERE project_id= ?",
                  [
                      comments,
                      project_id
                  ]
                  )
        conn.commit()
        row = read_project(project_id)
        comments = row["comments"]
        for item in comments:
            print(item)
            if (item["comment_id"] == data["comment_id"]):
                return item
        return None
    else:
        return None
