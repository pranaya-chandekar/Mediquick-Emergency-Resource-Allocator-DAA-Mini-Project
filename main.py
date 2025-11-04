import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

class Hospital:
    def _init_(self, name, x, y, capacity):
        self.name = name
        self.x = x
        self.y = y
        self.capacity = capacity
        self.current = 0

    def available(self):
        return self.current < self.capacity

class Ambulance:
    def _init_(self, id, x, y, available=True):
        self.id = id
        self.x = x
        self.y = y
        self.available = available

class Patient:
    def _init_(self, id, x, y, severity):
        self.id = id
        self.x = x
        self.y = y
        self.severity = severity

def distance(a, b):
    return math.sqrt((a.x - b.x) * 2 + (a.y - b.y) * 2)

def greedy_assign_ambulances(patients, ambulances):
    assignments = []
    for p in patients:
        nearest = None
        min_dist = float("inf")
        for amb in ambulances:
            if amb.available:
                d = distance(p, amb)
                if d < min_dist:
                    min_dist = d
                    nearest = amb
        if nearest:
            nearest.available = False
            assignments.append((p, nearest, min_dist))
    return assignments

def dp_assign_hospitals(patients, hospitals):
    n = len(patients)
    m = len(hospitals)
    dp = [[float("inf")] * (m + 1) for _ in range(n + 1)]
    dp[0] = [0] * (m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if not hospitals[j - 1].available():
                continue
            dist_cost = distance(patients[i - 1], hospitals[j - 1])
            load_penalty = hospitals[j - 1].current * 2
            best_prev = min(dp[i - 1]) + dist_cost + load_penalty
            dp[i][j] = best_prev
    result = []
    for i in range(1, n + 1):
        best_j = min(
            range(1, m + 1),
            key=lambda j: dp[i][j] if hospitals[j - 1].available() else float("inf"),
        )
        result.append((patients[i - 1], hospitals[best_j - 1]))
        hospitals[best_j - 1].current += 1
    return result

def backtrack_reallocate(assignments, hospitals):
    for i, (p, h) in enumerate(assignments):
        if not h.available():
            for alt in hospitals:
                if alt.available():
                    assignments[i] = (p, alt)
                    h.current -= 1
                    alt.current += 1
                    break
    return assignments

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
        hospital_names = ["CityCare", "MediHope", "LifeAid", "HealWell", "CarePlus"]
        random.shuffle(hospital_names)
        num_hospitals = random.randint(2, 4)
        self.hospitals = [Hospital(hospital_names[i], random.randint(0, 15), random.randint(0, 10), random.randint(1, 3)) for i in range(num_hospitals)]
        num_ambulances = random.randint(3, 6)
        self.ambulances = [Ambulance(f"A{i}", random.randint(0, 15), random.randint(0, 10)) for i in range(num_ambulances)]
        num_patients = random.randint(3, 8)
        self.patients = [Patient(f"P{i}", random.randint(0, 15), random.randint(0, 10), random.randint(1, 10)) for i in range(num_patients)]
        self.log("🧾 New Simulation Started...\n")
        self.log(f"🏥 Hospitals ({num_hospitals} total):")
        for h in self.hospitals:
            self.log(f"  • {h.name} at ({h.x},{h.y}), capacity={h.capacity}")
        self.log(f"\n🚑 Ambulances ({num_ambulances} total):")
        for a in self.ambulances:
            self.log(f"  • {a.id} at ({a.x},{a.y})")
        self.log(f"\n🧍 Patients ({num_patients} total):")
        for p in self.patients:
            self.log(f"  • {p.id} at ({p.x},{p.y}), severity={p.severity}")
        self.log("\n[1] Assigning ambulances (Greedy)...")
        amb_assign = greedy_assign_ambulances(self.patients, self.ambulances)
        for p, a, d in amb_assign:
            self.log(f"  {a.id} → {p.id} (distance={d:.2f})")
        self.log("\n[2] Assigning hospitals (Dynamic Programming)...")
        hosp_assign = dp_assign_hospitals(self.patients, self.hospitals)
        for p, h in hosp_assign:
            self.log(f"  {p.id} → {h.name}")
        self.log("\n[3] Checking overloaded hospitals (Backtracking)...")
        hosp_assign = backtrack_reallocate(hosp_assign, self.hospitals)
        for p, h in hosp_assign:
            self.log(f"  ✅ Final: {p.id} → {h.name}")
        self.assignments = hosp_assign
        self.log("\n✅ Allocation complete.\n")

    def reallocate(self):
        if not self.assignments:
            messagebox.showinfo("Info", "Run simulation first.")
            return
        self.log("\n♻ Reallocation (Ambulances returning + new updates)...")
        delivered = random.sample(self.assignments, k=random.randint(1, len(self.assignments)))
        for p, h in delivered:
            self.log(f"  ✅ {p.id} safely arrived at {h.name}.")
            for amb in self.ambulances:
                if not amb.available:
                    amb.available = True
                    self.log(f"  🚑 {amb.id} is now available for new patients.")
                    break
        if random.random() < 0.6:
            new_patient = Patient(f"P{len(self.patients)}", random.randint(0, 15), random.randint(0, 10), random.randint(1, 10))
            self.patients.append(new_patient)
            self.log(f"  🆕 New emergency: {new_patient.id} at ({new_patient.x},{new_patient.y}), severity={new_patient.severity}")
        for h in self.hospitals:
            if random.random() < 0.3 and h.current > 0:
                h.current -= 1
                self.log(f"  ⚠️ {h.name} freed 1 bed.")
        amb_assign = greedy_assign_ambulances(self.patients, self.ambulances)
        for p, a, d in amb_assign:
            self.log(f"  🚑 {a.id} → {p.id} (distance={d:.2f})")
        self.assignments = dp_assign_hospitals(self.patients, self.hospitals)
        for p, h in self.assignments:
            self.log(f"  🏥 {p.id} → {h.name}")
        self.assignments = backtrack_reallocate(self.assignments, self.hospitals)
        self.log("\n🔁 Backtracking reallocation complete — overloaded hospitals balanced.")
        for p, h in self.assignments:
            self.log(f"  🏥 Final: {p.id} → {h.name}")
        self.log("\n✅ Reallocation complete.\n")

if _name_ == "_main_":
    root = tk.Tk()
    app = MediQuickUI(root)
    root.mainloop()
