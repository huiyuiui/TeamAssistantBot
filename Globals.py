import json
import os

def initialize(): 
    global todo_list
    todo_list = {}

def read_todo_from_file(group_id):
    print("Called read_todo_from_file")

    global todo_list
    if(os.path.exists(f"todo_lists/todo_list_{group_id}.json")):
        with open(f"todo_lists/todo_list_{group_id}.json", "r") as f:
            todo_list = json.load(f)
            print(todo_list)

def get_todo_list():
    global todo_list
    try:
        return todo_list
    except:
        return {}

def update_todo_list(newList):
    print("Called update_todo_list")
    global todo_list
    todo_list = newList

def write_todo_to_file(group_id):
    global todo_list
    with open(f"todo_lists/todo_list_{group_id}.json", "w") as f:
        json.dump(todo_list, f)
