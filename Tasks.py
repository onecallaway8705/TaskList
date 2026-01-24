import os
import json
from pathlib import Path
import datetime

#----------------------
# Terminal coloring
#----------------------
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

#----------------------
# Utility functions
#----------------------
def clear():
    # Clears terminal screen
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")

def pause():
    # Pauses until Enter is pressed
    input("\nPress Enter to return to the main menu...")
    clear()

def ensure_tasks(state):
    # Returns True if tasks exists; otherwise prints message and returns False
    if not state["tasks"]:
        print("No tasks available.")
        pause()
        return False
    return True

def select_task(tasks, state):
    # Allows easier selection of task for completion and deletion
    column_label = "Phase" if state.get("mode") == "phase" else "Due Date"
    task_list = list(tasks.keys())
    for i, task in enumerate(task_list, start=1):
        value, status = tasks[task]
        print(f"{i}) [{status}] {task} ({column_label} {value})")
    while True:
        choice = input("Select task number (q to cancel): ").strip().lower()
        if choice == "q":
            return None        
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index <len(task_list):
                return task_list[index]            
        print("Invalid selection.")

#----------------------
# Core functions
#----------------------
def save(state):
    # Saves list to disk with backups
    file_path = state["file_path"]
    temp_path = file_path.with_suffix(".tmp")
    backup1 = file_path.with_suffix(".bak1")
    backup2 = file_path.with_suffix(".bak2")
    backup3 = file_path.with_suffix(".bak3")
    data = {
        "mode": state.get("mode", "due"),
        "tasks": state["tasks"]
    }
    with open(temp_path, "w") as f:
        json.dump(data, f, indent=4)
    if backup3.exists():
        backup3.unlink()
    if backup2.exists():
        backup2.rename(backup3)
    if backup1.exists():
        backup1.rename(backup2)
    if file_path.exists():
        file_path.rename(backup1)
    temp_path.rename(file_path)

def load(state):
    # Loads list from saves only if file exists
    tasks = {}
    mode = "due" # default
    directory_path = Path("lists")
    directory_path.mkdir(exist_ok=True)
    json_list = [item.stem for item in directory_path.glob("*.json")]
    if json_list:
        print("Available lists:", ", ".join(json_list))
    else:
        print("No saved lists found.")
    list_name = input("Select Task list to load/create (default:tasks): ").strip().lower()
    if list_name == "":
        list_name = "tasks"
    file_path = directory_path / Path(list_name).with_suffix(".json")
    clear()
    def try_load(file):
        #attempt to load JSON file
        with open(file, "r") as f:
            data = json.load(f)
            if "tasks" in data:
                tasks = data["tasks"]
                mode = data.get("mode", "due")
            else:
                tasks= data
                mode = "due"
            return tasks, mode
    loaded_valid_file = False
    if file_path.exists():
        try:
            tasks, mode = try_load(file_path)
            loaded_valid_file = True
        except (json.JSONDecodeError, OSError):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            corrupt_backup = file_path.with_name(f"{file_path.stem}_CORRUPT_{timestamp}.json")
            file_path.rename(corrupt_backup)
            print(f"Main save is corrupted. Saved as {corrupt_backup.name}.")
            loaded_backup = False
            for bak_suffix in ["bak1", "bak2", "bak3"]:
                backup_file = directory_path / f"{list_name}.{bak_suffix}"
                if backup_file.exists():
                    try:
                        tasks, mode = try_load(backup_file)
                        print(f"Loaded backup {backup_file.name} successfully.")
                        loaded_backup = True
                        loaded_valid_file = True
                        break
                    except (json.JSONDecodeError, OSError):
                        print(f"Backup {backup_file.name} is also corrupted.")
                        continue
            if not loaded_backup:
                print("No valid backup found. Starting empty list.")
                pause()
    if not loaded_valid_file:
        mode_choice = input("Select mode for new list(1=Due Date, 2=Phase, default=Due Date: ")
        if mode_choice == "2":
            mode = "phase"
        else:
            mode = "due"
    state["tasks"] = tasks
    state["file_path"] = file_path
    state["list_name"] = list_name
    state["mode"] = mode
    

def new_list(state):
    # Loads new list after prompting for save
    list_save = input("Save current changes? (y/N): ").strip().lower()
    if list_save == "y":
        save(state)
    load(state)

#----------------------
# Task Operations
#----------------------
def view(state):
    tasks = state["tasks"]
    mode = state.get("mode", "due")
    if mode == "phase":
        column_label = "Phase"
    else:
        column_label = "Due Date"
    # Prints tasks in a formatted sortable table
    if not ensure_tasks(state):
        return
    column_map = {"1": 0, "2": 1, "3": "key"}
    choice = input(f"Sort by column (1={column_label}, 2=Completed, 3=Task Name): ")
    if choice in column_map:
        if column_map[choice] == "key":
            sorted_tasks = sorted(tasks.items(), key=lambda item: item[0])
        else:
            sorted_tasks = sorted(tasks.items(), key=lambda item: item[1][column_map[choice]])
    else:
        sorted_tasks = tasks.items()
    if choice == "1":
        headers = [f"{column_label}(v)", "Completed", "Task"]
    elif choice == "2":
        headers = [f"{column_label}", "Completed(v)", "Task"]
    elif choice == "3":
        headers = [f"{column_label}", "Completed", "Task(v)"]
    else:
        headers = [f"{column_label}", "Completed", "Task"]
    header_format = "{:<15} {:<15} {:<15}"
    print(header_format.format(*headers))
    print("-" * 45)
    for key, values in sorted_tasks:
        due, complete = values
        formatted_complete = f"{str(complete):<15}"
        formatted_due = f"{str(due):<15}"
        formatted_key = f"{str(key):<15}"
        if complete == "Yes":
            complete_display = f"{GREEN}{formatted_complete}{RESET}"
        else:
            complete_display = f"{RED}{formatted_complete}{RESET}"
        print(formatted_due, complete_display, formatted_key)
    pause()

def add(state):
    tasks = state["tasks"]
    column_label = "Phase" if state.get("mode") == "phase" else "Due Date"
    # Adds new task entry to loaded list, prompts additional entries, and saves file
    while True:
        while True:
            print("q to go back")
            user_task = input("Task title: ").strip()
            if user_task == "":
                print("Task cannot be empty!")
            elif user_task == "q":
                clear()
                return
            else:
                break
        while True:
            print("q to go back")
            user_value = input(f"{column_label}: ").strip()
            if user_value == "":
                print(f"{column_label} cannot be empty!")
            elif user_value == "q":
                clear()
                return
            else:
                break
        tasks[f"{user_task}"] = [f"{user_value}", "No"]
        print(f"{user_task}: {column_label} {user_value}")
        add_more = input("Add another task? (y/N): ").strip().lower()
        clear()
        if add_more != "y":
            save(state)
            return
        
def complete(state):
    tasks = state["tasks"]
    # Mark task as completed
    if not ensure_tasks(state):
        return
    while True:
        print("\nSelect task to mark complete:")
        task = select_task(tasks, state)
        if task is None:
            clear()
            return
        tasks[task][1] = "Yes"
        print(f"{task} marked complete!")
        more = input("Complete another task? (y/N): ").strip().lower()
        clear()
        if more != "y":
            save(state)
            return

def delete(state):
    tasks = state["tasks"]
    # Remove task entry from list with confirmation
    if not ensure_tasks(state):
        return
    while True:
        print("\nSelect task to delete:")
        task = select_task(tasks, state)
        if task is None:
            clear()
            return
        confirm = input(f"Delete '{task}'? (y/N): ").strip().lower()
        if confirm == "y":
            tasks.pop(task)
            print(f"{task} deleted.")
        else:
            print("Deletion cancelled.")
        more = input("Delete more tasks? (y/N): ")
        clear()
        if more != "y":  
            save(state)          
            return 

#----------------------
# Main Menu
#----------------------

def main(state):
    while True:
        print(f"--Tasks List-- ({GREEN}{state['list_name']}{RESET})")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Load new list")
        print("6. Save and Continue")
        print("7. Save and Exit")
        choice = input("Select 1-7: ")
        if choice == "1":
            clear()
            view(state)      
        elif choice == "2":
            clear()
            add(state)        
        elif choice == "3":
            clear()
            complete(state)
        elif choice == "4":
            clear()
            delete(state)
        elif choice == "5":
            new_list(state)
        elif choice == "6":
            clear()
            save(state)
            print("Saving")
            pause()
        elif choice == "7":
            clear()
            save(state)
            print("Saving and Exiting")
            break
        else:
            clear()
            print("Please select 1-7")

#----------------------
# Startup
#----------------------

clear()
state = {
    "tasks": {},
    "file_path": None,
    "list_name": None,
    "mode": "due" #or "phase"
}
load(state)
main(state)