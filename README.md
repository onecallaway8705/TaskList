Project Name: Terminal Task Manager

Overview

This is a Python terminal-based task manager that lets you:
Create, view, complete, and delete tasks.
Organize tasks by Due Date or Phase.
Store tasks in JSON files with automatic backups.
Sort tasks by columns and color-code completed tasks.
It’s lightweight, portable, and works entirely in the terminal.

Features

Add tasks with due dates or numeric phases.
Mark tasks as complete.
Delete tasks with confirmation.
Save and load multiple task lists.
Automatic backup system (.bak1, .bak2, .bak3) for corrupted files.
Color-coded task completion (Yes = green, No = red).
Supports sorting by Task Name, Due Date/Phase, or Completion status.

Usage

View Tasks: Display all tasks with sorting options.
Add Task: Add a new task with a due date or numeric phase.
Complete Task: Mark tasks as complete.
Delete Task: Remove tasks with confirmation.
Load new list: Switch between different JSON task lists.
Save and Continue / Save and Exit: Save changes to disk.

JSON Format

Tasks are stored in JSON files. Examples:

Due Date format:
```
{
    "mode": "due",
    "tasks": {
            "Buy groceries": [
            "1/23",
            "No"
        ],
        "Call Alice": [
            "1/25",
            "No"
        ]
    }
}
```
Phase format:
```
{
    "mode": "phase",
    "tasks": {
        "Define bot scope and permissions": [
            1,
            "No"
        ],
        "Design database schema": [
            3,
            "No"
        ]
    }
}
```

Backup System

Saves automatically create backups: .bak1, .bak2, .bak3.
If the main file is corrupted, it will attempt to load the most recent valid backup.
Corrupted files are renamed with _CORRUPT_TIMESTAMP.json.

Requirements

Python 3.x
Works in terminal environments (Windows, Linux, macOS)
