from collections import deque


class TrendAnalyzer:


    def __init__(self, window=10):

        self.history = {}

        self.window = window



    def add(self, node_id, hazard):

        if node_id not in self.history:

            self.history[node_id] = deque(
                maxlen=self.window
            )


        self.history[node_id].append(
            hazard
        )



    def get_rate(self,node_id):

        if node_id not in self.history:
            return 0


        values = list(
            self.history[node_id]
        )


        if len(values) < 2:
            return 0


        old = values[0]

        new = values[-1]


        return (new-old)/(len(values)-1)



    def get_history(self,node_id):

        return list(
            self.history.get(
                node_id,
                []
            )
        )