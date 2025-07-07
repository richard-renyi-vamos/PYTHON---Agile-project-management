from datetime import datetime

class Task:
    def __init__(self, title, description, assignee=None):
        self.title = title
        self.description = description
        self.assignee = assignee
        self.status = "To Do"
        self.created_at = datetime.now()

    def update_status(self, new_status):
        if new_status in ["To Do", "In Progress", "Done"]:
            self.status = new_status
        else:
            print("❌ Invalid status!")

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

    def sprint_status(self):
        status_count = {"To Do": 0, "In Progress": 0, "Done": 0}
        for task in self.tasks:
            status_count[task.status] += 1
        return status_count

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
    task1 = Task("Setup CI/CD", "Configure Jenkins and Docker", "Alice")
    task2 = Task("Database Schema", "Design initial DB schema", "Bob")
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

    # Show sprint board
    sprint1.show_board()

    # Print sprint status summary
    print("\n📊 Sprint Progress:", sprint1.sprint_status())
