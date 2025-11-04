import tkinter as tk
from tkinter import ttk, messagebox
import random

class MediQuickUI:
    def _init_(self, root):
        self.root = root
        self.root.title("🚑 MediQuick: Emergency Resource Allocator")
        self.root.geometry("980x700")
        self.root.configure(bg="#f4f9fb")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Helvetica", 12, "bold"), padding=10, background="#a3d5e0", foreground="#00333f", borderwidth=0)
        style.map("TButton", background=[("active", "#7bc0ce")])
        style.configure("TLabel", background="#f4f9fb", foreground="#003d4d")

        header_frame = tk.Frame(root, bg="#c6ecf1", height=70)
        header_frame.pack(fill="x")
        title_label = tk.Label(header_frame, text="🚑 MediQuick: Emergency Resource Allocator", font=("Helvetica", 20, "bold"), fg="#004d60", bg="#c6ecf1")
        title_label.pack(pady=15)

        button_frame = ttk.Frame(root)
        button_frame.pack(pady=15)
        ttk.Button(button_frame, text="▶ Run Simulation", command=self.run_simulation).grid(row=0, column=0, padx=15)
        ttk.Button(button_frame, text="♻ Reallocate Resources", command=self.reallocate).grid(row=0, column=1, padx=15)

        output_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
        output_frame.pack(fill="both", expand=True, padx=25, pady=15)
        text_frame = tk.Frame(output_frame, bg="white")
        text_frame.pack(fill="both", expand=True)
        self.text = tk.Text(text_frame, wrap="word", bg="#fbfdfd", fg="#002b36", font=("Consolas", 11), relief="flat", padx=10, pady=10)
        self.text.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(text_frame, command=self.text.yview)
        scrollbar.pack(side="right", fill="y")
        self.text.config(yscrollcommand=scrollbar.set)

        self.hospitals, self.ambulances, self.patients = [], [], []
        self.assignments = []

    def log(self, msg):
        self.text.insert(tk.END, msg + "\n")
        self.text.see(tk.END)

    def run_simulation(self):
        self.text.delete(1.0, tk.END)
        self.log("Simulation Running... (Algorithm logic will go here)")

    def reallocate(self):
        messagebox.showinfo("Info", "Reallocation logic will go here.")

if _name_ == "_main_":
    root = tk.Tk()
    app = MediQuickUI(root)
    root.mainloop()
