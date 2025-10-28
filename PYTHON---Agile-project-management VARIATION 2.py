import json
import os
from datetime import datetime

# --- Configuration ---
DATA_FILE = "agile_data.json"
STATUSES = ["To Do", "In Progress", "Done"]

class Task:
    """Represents a single user story or task."""
    def __init__(self, title, description, status="To Do", task_id=None):
        self.id = task_id if task_id is not None else self._generate_id()
        self.title = title
        self.description = description
        self.status = status
        self.created_at = datetime.now().isoformat()

    def _generate_id(self):
        """Generates a simple timestamp-based ID."""
        return int(datetime.now().timestamp() * 1000)

    def to_dict(self):
        """Converts the Task object to a dictionary for saving."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Task object from a dictionary loaded from storage."""
        task = cls(data['title'], data['description'], data['status'], data['id'])
        task.created_at = data['created_at']
        return task

    def __str__(self):
        """String representation for display."""
        return f"ID: {self.id} | Status: {self.status:<12} | Title: {self.title}"

class ProjectManager:
    """Manages all tasks and data persistence."""
    def __init__(self):
        self.tasks = []
        self._load_data()

    def _load_data(self):
        """Loads tasks from the JSON file."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(d) for d in data.get("tasks", [])]
                print(f"Data loaded successfully from {DATA_FILE}. Total tasks: {len(self.tasks)}")
            except json.JSONDecodeError:
                print(f"Warning: Could not decode {DATA_FILE}. Starting with an empty state.")
                self.tasks = []
        else:
            print(f"No existing data file ({DATA_FILE}) found. Starting fresh.")

    def _save_data(self):
        """Saves current tasks to the JSON file."""
        data = {"tasks": [t.to_dict() for t in self.tasks]}
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {DATA_FILE}.")

    def add_task(self, title, description):
        """Adds a new task to the backlog (default status 'To Do')."""
        new_task = Task(title, description)
        self.tasks.append(new_task)
        self._save_data()
        print(f"\n✨ Task '{title}' added with ID: {new_task.id}.")

    def get_task_by_id(self, task_id):
        """Finds a task by its ID."""
        try:
            task_id = int(task_id)
            return next((t for t in self.tasks if t.id == task_id), None)
        except ValueError:
            return None

    def display_board(self):
        """Displays the Agile board (Kanban style)."""
        print("\n" + "="*80)
        print("          ✨ AGILE PROJECT BOARD (Kanban View) ✨")
        print("="*80)

        # Group tasks by status
        board = {status: [] for status in STATUSES}
        for task in self.tasks:
            board[task.status].append(task)

        # Print columns
        for status in STATUSES:
            print(f"\n--- {status.upper()} ({len(board[status])}) ---")
            if not board[status]:
                print("  (No tasks in this column)")
            for task in board[status]:
                print(f"  [{task.id}] {task.title}")
        print("="*80 + "\n")

    def update_task_status(self, task_id, new_status):
        """Updates the status of an existing task."""
        task = self.get_task_by_id(task_id)
        if task:
            if new_status in STATUSES:
                if task.status != new_status:
                    task.status = new_status
                    self._save_data()
                    print(f"\n✅ Task {task_id} status updated to '{new_status}'.")
                else:
                    print(f"\nℹ️ Task {task_id} is already in status '{new_status}'.")
            else:
                print(f"\n❌ Invalid status '{new_status}'. Must be one of: {', '.join(STATUSES)}")
        else:
            print(f"\n❌ Error: Task with ID '{task_id}' not found.")

def print_help():
    """Prints the available commands."""
    print("\n" + "~"*30)
    print("AGILE CLI COMMANDS")
    print("~"*30)
    print("  add    - Add a new task (e.g., 'add New Feature Title')")
    print("  move   - Change a task's status (e.g., 'move 1234567890 To Done')")
    print("  board  - Display the current Agile board (Kanban)")
    print("  list   - List all available statuses")
    print("  help   - Show this help message")
    print("  exit   - Save and exit the application")
    print("~"*30 + "\n")


def main():
    """Main function for the CLI application loop."""
    manager = ProjectManager()
    print("\n--- Welcome to the Python Agile Project Manager ---")
    print_help()

    while True:
        try:
            user_input = input("PM > ").strip()
            if not user_input:
                continue

            parts = user_input.split(maxsplit=2)
            command = parts[0].lower()

            if command == "exit":
                print("Goodbye! All tasks have been saved.")
                break

            elif command == "help":
                print_help()

            elif command == "list":
                print("\nAvailable Statuses: " + ", ".join(STATUSES))

            elif command == "board":
                manager.display_board()

            elif command == "add":
                if len(parts) < 2:
                    print("Usage: add <Title of Task> (Press ENTER for description)")
                    continue

                title = parts[1]
                description = input(f"Enter description for '{title}': ").strip()
                manager.add_task(title, description)

            elif command == "move":
                if len(parts) < 3:
                    print(f"Usage: move <Task ID> <New Status> (Statuses: {', '.join(STATUSES)})")
                    continue

                task_id_str = parts[1]
                new_status = parts[2]
                manager.update_task_status(task_id_str, new_status)

            else:
                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # Ensure data is saved even on error before re-looping
            manager._save_data()
            print("Please try again.")

if __name__ == "__main__":
    main()
