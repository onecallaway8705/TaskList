import os
import json
from pathlib import Path
#Creates main menu
def main():
    while True:
        print(f"--Tasks List-- ({GREEN}{list_name}{RESET})")
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
            view()      
        elif choice == "2":
            clear()
            add()        
        elif choice == "3":
            clear()
            complete()
        elif choice == "4":
            clear()
            delete()
        elif choice == "5":
            new_list()
        elif choice == "6":
            clear()
            save()
            print("Saving")
            pause()
        elif choice == "7":
            clear()
            save()
            print("Saving and Exiting")
            break
        else:
            clear()
            print("Please select 1-7")
#clears terminal to keep things tidy            
def clear():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")
#prints a sorted/unsorted table of all tasks saved
def view():
    if not ensure_tasks():
        return
    column_map = {"1": 0, "2": 1, "3": "key"}
    choice = input("Sort by column (1=Due Date, 2=Completed, 3=Task Name): ")
    if choice in column_map:
        if column_map[choice] == "key":
            sorted_tasks = sorted(tasks.items(), key=lambda item: item[0])
        else:
            sorted_tasks = sorted(tasks.items(), key=lambda item: item[1][column_map[choice]])
    else:
        sorted_tasks = tasks.items()
    if choice == "1":
        headers = ["Due Date(v)", "Completed", "Task"]
    elif choice == "2":
        headers = ["Due Date", "Completed(v)", "Task"]
    elif choice == "3":
        headers = ["Due Date", "Completed", "Task(v)"]
    else:
        headers = ["Due Date", "Completed", "Task"]
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
        row = [formatted_due, complete_display, formatted_key]
        print("".join(f"{str(item):<{15}}" for item in row))
    pause()
#creates new task entry with error handling        
def add():
    while True:
        while True:
            print("q to go back")
            user_task = input("Task title: ").strip().lower()
            if user_task == "":
                print("Task cannot be empty!")
            elif user_task == "q":
                return
            else:
                break
        while True:
            print("q to go back")
            user_due = input("Due date: ").strip().lower()
            if user_due == "":
                print("Due date cannot be empty!")
            elif user_due == "q":
                return
            else:
                break
        tasks[f"{user_task}"] = [f"{user_due}", "No"]
        print(f"{user_task}: created and is due {user_due}")
        add_more = input("Add another task? (y/N): ").strip().lower()
        clear()
        if add_more != "y":
            return
#marks task as completed    
def complete():
    if not ensure_tasks():
        return
    while True:
        print("q to go back")
        print(", ".join(sorted(tasks)))
        user_complete = input("Task to mark complete: ").strip().lower()
        if user_complete in tasks:
            tasks[user_complete][1] = "Yes"
            print(f"{user_complete} has been marked complete!")
            complete_more = input("Complete another task? (y/N): ").strip().lower()
            clear()
            if complete_more != "y":
                return        
        elif user_complete == "q":
            clear()
            return
        else:
            clear()
            print(f"{user_complete} does not exist!")
#Removes task from the list with a confimation        
def delete():
    if not ensure_tasks():
        return
    while True:
        print("q to go back")
        print(", ".join(sorted(tasks)))
        remove_task = input("Task to be deleted: ").strip().lower()
        if remove_task in tasks:
            confirm = input(f"Are you sure you wish to delete {remove_task}? (y/n):").strip().lower()
            if confirm == "y":
                tasks.pop(remove_task)
                print(f"Deleting task {remove_task}")
                delete_more = input("Delete more tasks? (y/N): ")
                clear()
                if delete_more != "y":            
                    return 
            else:
                print("Deletion cancelled!")
        elif remove_task == "q":
            clear()
            return
        else:
            clear()
            print(f"{remove_task} does not exist")
def pause():
    input("\nPress Enter to return to the main menu...")
    clear()
def ensure_tasks():
    if not tasks:
        print("No tasks available.")
        pause()
        return False
    return True
def new_list():
    global file_path, list_name, tasks
    list_save = input("Save current changes? (y/N): ").strip().lower()
    if list_save == "y":
        save()
    file_path, list_name, tasks = load()

#scans for list files to load
def load():
    directory_path = Path("lists")
    directory_path.mkdir(exist_ok=True)
    json_list = [item.stem for item in directory_path.glob("*.json")]
    if json_list:
        print("Available lists", ", ".join(json_list))
    else:
        print("No saved lists found.")
    list_name = input("Select Task list to load/create (default:tasks): ").strip().lower()
    if list_name == "":
        list_name = "tasks"
    file_path = directory_path / Path(list_name).with_suffix(".json")
    clear()
    if file_path.exists():
        tasks = {}
        try:
            with open(file_path, "r") as f:
                tasks = json.load(f)
        except (json.JSONDecodeError, OSError):
            print("List file is corrupted. Starting empty.")
            tasks = {}
            pause()
    else:
        tasks = {}
    return file_path, list_name, tasks
#saves dictionary to disk        
def save():
    with open(file_path, "w") as f:
        json.dump(tasks, f, indent=4)
#loads dictionary from disk only if it exists
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
clear()

file_path, list_name, tasks = load()

main()