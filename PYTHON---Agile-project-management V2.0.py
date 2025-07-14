from datetime import datetime, timedelta

class Task:
    def __init__(self, title, description, assignee=None, due_date=None):
        self.title = title
        self.description = description
        self.assignee = assignee
        self.status = "To Do"
        self.created_at = datetime.now()
        self.due_date = due_date  # Optional due date

    def update_status(self, new_status):
        if new_status in ["To Do", "In Progress", "Done"]:
            self.status = new_status
        else:
            print("❌ Invalid status!")

    def reassign_task(self, new_assignee):
        self.assignee = new_assignee
        print(f"🔄 Task '{self.title}' reassigned to {new_assignee}")

    def is_overdue(self):
        return self.due_date and datetime.now() > self.due_date and self.status != "Done"

    def __repr__(self):
        return f"{self.title} [{self.status}] - {self.assignee if self.assignee else 'Unassigned'}"


class Sprint:
    def __init__(self, name, start_date, end_date):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, title):
        task = self.get_task_by_title(title)
        if task:
            self.tasks.remove(task)
            print(f"🗑️ Task '{title}' removed.")
        else:
            print("❌ Task not found!")

    def get_task_by_title(self, title):
        for task in self.tasks:
            if task.title.lower() == title.lower():
                return task
        return None

    def sprint_status(self):
        status_count = {"To Do": 0, "In Progress": 0, "Done": 0}
        for task in self.tasks:
            status_count[task.status] += 1
        return status_count

    def get_overdue_tasks(self):
        return [task for task in self.tasks if task.is_overdue()]

    def list_all_tasks(self):
        print(f"\n📋 All Tasks in {self.name}:")
        for task in self.tasks:
            print(f"  - {task}")

    def show_board(self):
        print(f"\n📆 Sprint: {self.name}")
        print("🔹 To Do:")
        for task in self.tasks:
            if task.status == "To Do":
                print(f"  - {task}")
        print("🔸 In Progress:")
        for task in self.tasks:
            if task.status == "In Progress":
                print(f"  - {task}")
        print("✅ Done:")
        for task in self.tasks:
            if task.status == "Done":
                print(f"  - {task}")

# Example Usage:
if __name__ == "__main__":
    # Create Tasks
    task1 = Task("Setup CI/CD", "Configure Jenkins and Docker", "Alice", datetime(2025, 7, 15))
    task2 = Task("Database Schema", "Design initial DB schema", "Bob", datetime(2025, 7, 10))
    task3 = Task("Login Page", "Develop frontend login", "Carol")

    # Create Sprint
    sprint1 = Sprint("Sprint 1", "2025-07-08", "2025-07-22")

    # Add tasks to sprint
    sprint1.add_task(task1)
    sprint1.add_task(task2)
    sprint1.add_task(task3)

    # Update task statuses
    task1.update_status("In Progress")
    task2.update_status("Done")

    # Reassign task
    task3.reassign_task("David")

    # Show sprint board
    sprint1.show_board()

    # Print sprint status summary
    print("\n📊 Sprint Progress:", sprint1.sprint_status())

    # List all tasks
    sprint1.list_all_tasks()

    # Check overdue tasks
    print("\n⏰ Overdue Tasks:")
    overdue = sprint1.get_overdue_tasks()
    for task in overdue:
        print(f"  - {task}")
