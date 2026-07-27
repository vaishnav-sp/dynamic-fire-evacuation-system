class DashboardState:


    def __init__(self):

        self.state = {

            "nodes": {},

            "evacuation": {},

            "routes": {}

        }



    def update_nodes(self, nodes):

        self.state["nodes"] = nodes



    def update_evacuation(self, data):

        self.state["evacuation"] = data



    def update_routes(self, data):

        self.state["routes"] = data



    def get_state(self):

        return self.state