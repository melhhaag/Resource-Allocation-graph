class DeadlockAvoidance:
    def __init__(self, available, max_demand, allocation):
        self.available = available
        self.max_demand = max_demand
        self.allocation = allocation
        self.need = [[self.max_demand[i][j] - self.allocation[i][j] for j in range(len(self.max_demand[0]))] for i in range(len(self.max_demand))]

    def is_safe_state(self):
        work = self.available[:]
        finish = [False] * len(self.allocation)

        while True:
            found = False
            for i in range(len(self.allocation)):
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(len(work))):
                    for k in range(len(work)):
                        work[k] += self.allocation[i][k]
                    finish[i] = True
                    found = True

            if not found:
                break

        return all(finish)

    def request_resources(self, process_number, request):
        if any(request[j] > self.need[process_number][j] for j in range(len(request))):
            return False, "Error: Process has exceeded its maximum claim."

        if any(request[j] > self.available[j] for j in range(len(request))):
            return False, "Error: Resources are not available."

        for j in range(len(request)):
            self.available[j] -= request[j]
            self.allocation[process_number][j] += request[j]
            self.need[process_number][j] -= request[j]

        if self.is_safe_state():
            return True, "Resources allocated."
        else:
            for j in range(len(request)):
                self.available[j] += request[j]
                self.allocation[process_number][j] -= request[j]
                self.need[process_number][j] += request[j]
            return False, "Resources allocation failed. System would be in an unsafe state."
