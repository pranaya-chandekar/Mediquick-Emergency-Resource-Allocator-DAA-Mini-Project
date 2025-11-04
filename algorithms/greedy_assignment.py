import math

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
