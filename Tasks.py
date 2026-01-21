import os
import json
def main():
    while True:
        print("--Tasks List--")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Save and Exit")
        choice = input("Select 1-5: ")
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
            clear()
            save()
            print("Saving and Exiting")
            break
        else:
            clear()
            print("Please select 1-5")
def clear():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")
def view():
    column_map = {"1": 0, "2": 1, "3": "key"}
    choice = input("Sort by column (1=Due Date, 2=Completed, 3=Task Name): ")
    if choice in column_map:
        if column_map[choice] == "key":
            sorted_tasks = sorted(tasks.items(), key=lambda item: item[0])
        else:
            sorted_tasks = sorted(tasks.items(), key=lambda item: item[1][column_map[choice]])
    else:
        sorted_tasks = tasks.items()
    headers = ["Due Date", "Completed", "Task"]
    header_format = "{:<15} {:<15} {:<15}"
    print(header_format.format(*headers))
    print("-" * 45)
    for key, values in sorted_tasks:
        due, complete = values
        row = [due, complete, key]
        print("".join(f"{str(item):<{15}}" for item in row))
def add():
    while True:
        print("q to go back")
        user_task = input("Task title: ").strip()
        if user_task == "":
            print("Task cannot be empty!")
        elif user_task == "q":
            main()
        else:
            break
    while True:
        print("q to go back")
        user_due = input("Due date: ").strip()
        if user_due == "":
            print("Due date cannot be empty!")
        elif user_due == "q":
            main()
        else:
            break
    tasks[f"{user_task}"] = [f"{user_due}", "No"]
    print(f"{user_task}: created and is due {user_due}")
def complete():
    keys_list = [*tasks]
    print("q to go back")
    print(keys_list)
    user_complete = input("Taks to mark complete: ")
    if user_complete in tasks:
        tasks[user_complete][1] = "Yes"
        print(f"{user_complete} has been marked complete!")
    elif user_complete == "q":
        clear()
        main()
    else:
        clear()
        print(f"{user_complete} does not exist!")
        complete()
def delete():
    keys_list = [*tasks]
    print("q to go back")
    print(keys_list)
    remove_task = input("Task to be deleted: ")
    if remove_task in tasks:
        confirm = input(f"Are you sure you wish to delete {remove_task}? (y/n):")
        if confirm.lower() == "y":
            tasks.pop(remove_task)
            print(f"Deleting task {remove_task}")
        else:
            print("Deletion cancelled!")
    elif remove_task == "q":
        clear()
        main()
    else:
        clear()
        print(f"{remove_task} does not exist")
        delete()
def save():
    file_path = "tasks.json"
    with open(file_path, "w") as f:
        json.dump(tasks, f, indent=4)
if os.path.exists("tasks.json"):
    tasks = {}
    file_path = "tasks.json"
    with open(file_path, "r") as f:
        tasks = json.load(f)
else:
    tasks = {}
main()