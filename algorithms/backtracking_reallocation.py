class Hospital:
    def _init_(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.current = 0

    def available(self):
        return self.current < self.capacity

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


if _name_ == "_main_":
    from Dynamic_Programming import Patient

    h1 = Hospital("CityCare", 1)
    h2 = Hospital("LifeAid", 2)
    h1.current = 1
    h2.current = 0

    p1 = Patient("P1", 2, 3, 7)
    p2 = Patient("P2", 5, 8, 4)

    assignments = [(p1, h1), (p2, h1)]
    result = backtrack_reallocate(assignments, [h1, h2])

    for p, h in result:
        print(f"✅ Final: {p.id} → {h.name}")
