import tkinter as tk
from tkinter import messagebox
from deadlock_detection import DeadlockDetection
from deadlock_avoidance import DeadlockAvoidance

class Deadlock:
    def __init__(self, root):
        self.root = root
        self.root.title("Deadlock Detection and Avoidance")
    
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Available Resources (space separated):").grid(row=0, column=0)
        self.available_entry = tk.Entry(self.root)
        self.available_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Max Demand Matrix (rows space separated, use ; to separate rows):").grid(row=1, column=0)
        self.max_demand_entry = tk.Entry(self.root)
        self.max_demand_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Allocation Matrix (rows space separated, use ; to separate rows):").grid(row=2, column=0)
        self.allocation_entry = tk.Entry(self.root)
        self.allocation_entry.grid(row=2, column=1)

        tk.Button(self.root, text="Detect Deadlock", command=self.detect_deadlock).grid(row=3, column=0)
        tk.Button(self.root, text="Avoid Deadlock", command=self.avoid_deadlock).grid(row=3, column=1)
        tk.Button(self.root, text="Clear", command=self.clear_inputs).grid(row=3, column=2)

        tk.Label(self.root, text="Process Number:").grid(row=4, column=0)
        self.process_number_entry = tk.Entry(self.root)
        self.process_number_entry.grid(row=4, column=1)

        tk.Label(self.root, text="Resource Request (space separated):").grid(row=5, column=0)
        self.request_entry = tk.Entry(self.root)
        self.request_entry.grid(row=5, column=1)

    def get_input(self):
        try:
            available = list(map(int, self.available_entry.get().strip().split()))
            max_demand = [list(map(int, row.strip().split())) for row in self.max_demand_entry.get().strip().split(';')]
            allocation = [list(map(int, row.strip().split())) for row in self.allocation_entry.get().strip().split(';')]
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")
            return None, None, None
        return available, max_demand, allocation

    def detect_deadlock(self):
        available, max_demand, allocation = self.get_input()
        if available is None:
            return
        detector = DeadlockDetection(available, max_demand, allocation)
        if detector.detect_deadlock():
            messagebox.showinfo("Result", "Deadlock detected")
        else:
            messagebox.showinfo("Result", "No deadlock detected")

    def avoid_deadlock(self):
        available, max_demand, allocation = self.get_input()
        if available is None:
            return
        avoidance = DeadlockAvoidance(available, max_demand, allocation)
        try:
            process_number = int(self.process_number_entry.get().strip())
            request = list(map(int, self.request_entry.get().strip().split()))
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")
            return
        success, message = avoidance.request_resources(process_number, request)
        messagebox.showinfo("Result", message)

    def clear_inputs(self):
        self.available_entry.delete(0, tk.END)
        self.max_demand_entry.delete(0, tk.END)
        self.allocation_entry.delete(0, tk.END)
        self.process_number_entry.delete(0, tk.END)
        self.request_entry.delete(0, tk.END)
 
if __name__ == "__main__":
    root = tk.Tk()
    app = Deadlock(root)
    root.mainloop()
