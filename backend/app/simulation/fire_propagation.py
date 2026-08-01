from collections import deque


class FirePropagation:

    def __init__(self, graph):

        self.graph = graph

        self.temperature_decay = 0.65
        self.smoke_decay = 0.80

        self.min_temperature = 5
        self.min_smoke = 5

    def propagate(self, source, temperature, smoke):

        propagated = {}

        visited = set()

        queue = deque()

        queue.append((source, temperature, smoke))

        while queue:

            node, temp, smk = queue.popleft()

            if node in visited:
                continue

            visited.add(node)

            propagated[node] = {
                "temperature": round(temp, 1),
                "smoke": round(smk, 1)
            }

            for neighbour in self.graph.neighbors(node):

                if neighbour in visited:
                    continue

                next_temp = temp * self.temperature_decay
                next_smoke = smk * self.smoke_decay

                if self.graph.nodes[neighbour]["type"] == "CORRIDOR":
                    next_smoke *= 1.20

                if next_temp < self.min_temperature and next_smoke < self.min_smoke:
                    continue

                queue.append(
                    (
                        neighbour,
                        next_temp,
                        next_smoke
                    )
                )

        return propagated