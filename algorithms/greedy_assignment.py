import math

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
    return math.sqrt((a.x - b.x)*2 + (a.y - b.y)*2)

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


if _name_ == "_main_":
    patients = [Patient("P1", 2, 3, 7), Patient("P2", 6, 1, 4)]
    ambulances = [Ambulance("A1", 1, 2), Ambulance("A2", 5, 4)]
    result = greedy_assign_ambulances(patients, ambulances)
    for p, a, d in result:
        print(f"{a.id} → {p.id} (distance={d:.2f})")
