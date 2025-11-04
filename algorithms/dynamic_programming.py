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

class Patient:
    def _init_(self, id, x, y, severity):
        self.id = id
        self.x = x
        self.y = y
        self.severity = severity

def distance(a, b):
    return math.sqrt((a.x - b.x)*2 + (a.y - b.y)*2)

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


if _name_ == "_main_":
    patients = [Patient("P1", 2, 4, 7), Patient("P2", 5, 8, 3)]
    hospitals = [
        Hospital("CityCare", 3, 4, 2),
        Hospital("MediHope", 7, 9, 1),
    ]
    result = dp_assign_hospitals(patients, hospitals)
    for p, h in result:
        print(f"{p.id} → {h.name}")
