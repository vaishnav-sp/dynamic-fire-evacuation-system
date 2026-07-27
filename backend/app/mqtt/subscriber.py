import json


import paho.mqtt.client as mqtt

from app.decision.actuator_manager import ActuatorManager
from app.routing.graph_builder import GraphBuilder
from app.config.settings import BUILDING_FILE, MQTT_BROKER

from app.routing.route_manager import RouteManager

from app.decision.evacuation_manager import EvacuationManager

from app.managers.building_manager import BuildingManager

from app.dashboard.dashboard_store import dashboard_state

from app.prediction.fire_predictor import FirePredictor




class MQTTSubscriber:


    def __init__(self):


        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )



        building, graph = GraphBuilder(
            BUILDING_FILE
        ).load()



        self.building = building



        self.building_manager = BuildingManager(
            building
        )



        self.route_manager = RouteManager(
            graph
        )



        self.evacuation_manager = EvacuationManager(
            self.route_manager
        )


        self.actuator_manager = ActuatorManager()


        self.predictor = FirePredictor()






    def on_connect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties
    ):


        print(
            "Connected to MQTT Broker"
        )


        client.subscribe(
            "building/node/#"
        )


        print(
            "Subscribed to building/node/#"
        )






    def on_disconnect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties
    ):


        print(
            "MQTT Disconnected:",
            reason_code
        )






    def on_message(
        self,
        client,
        userdata,
        msg
    ):


        try:


            print(
                "\nMQTT RECEIVED:",
                msg.topic
            )



            payload = msg.payload.decode()



            print(
                payload
            )



            data = json.loads(
                payload
            )



            node_id = data["node_id"]





            # -----------------------------
            # Hazard calculation
            # -----------------------------


            data["hazard"] = self.calculate_hazard(
                data
            )





            # -----------------------------
            # Prediction
            # -----------------------------


            self.predictor.update(
                node_id,
                data["hazard"]
            )



            prediction = self.predictor.predict(
                node_id
            )



            data["prediction"] = prediction.get(
                "prediction",
                {}
            )



            data["prediction_score"] = prediction.get(
                "ignition_probability",
                0
            )







            # -----------------------------
            # Update node
            # -----------------------------


            self.update_building_node(
                data
            )





            hazard_map = self.get_building_state()






            # -----------------------------
            # Routing update
            # -----------------------------


            self.route_manager.update(
                hazard_map
            )





            evacuation_status = self.evacuation_manager.update(
                hazard_map
            )



            blocked_nodes = evacuation_status.get(
                "blocked_nodes",
                []
            )





            route = self.route_manager.calculate_route(

                start=node_id,

                exits=[
                    "E1",
                    "E2"
                ],

                blocked_nodes=blocked_nodes

            )



            evacuation_status["route"] = route


            commands = self.actuator_manager.generate_commands(
                evacuation_status
            )


            evacuation_status["actuator_commands"] = commands




            # -----------------------------
            # Dashboard
            # -----------------------------


            dashboard_state.update_nodes(
                hazard_map
            )

            print(
                "UPDATED DASHBOARD:",
                dashboard_state.get_state()
            )


            dashboard_state.update_evacuation(
                evacuation_status
            )







            print(
                "\n-------------------------"
            )


            print(
                evacuation_status
            )


            print(

                f"{node_id} | "
                f"Hazard={data['hazard']:.2f}% | "
                f"Prediction={data['prediction_score']}%"

            )


            print(
                "-------------------------\n"
            )



        except Exception as e:


            print(
                "MQTT PROCESSING ERROR:",
                e
            )








    def calculate_hazard(
        self,
        data
    ):


        score = (

            data.get("temperature",0) * 0.25

            +

            data.get("smoke",0) * 0.45

            +

            (100 if data.get("flame") else 0) * 0.30

        )


        return min(
            score,
            100
        )







    def update_building_node(
        self,
        data
    ):


        node_id = data["node_id"]



        if node_id in self.building.rooms:


            node = self.building.rooms[node_id]



        elif node_id in self.building.corridors:


            node = self.building.corridors[node_id]



        else:


            print(
                "Unknown node:",
                node_id
            )


            return






        node.temperature = data["temperature"]

        node.smoke = data["smoke"]

        node.flame = data["flame"]

        node.occupancy = data["occupancy"]


        node.hazard_score = data["hazard"]


        node.predicted_hazard = data.get(
            "prediction_score",
            0
        )


        node.prediction = data.get(
            "prediction",
            {}
        )




        risk = max(

            node.hazard_score,

            node.predicted_hazard

        )



        if risk >= 75:


            node.state = "CRITICAL"



        elif risk >=50:


            node.state = "DANGER"



        elif risk >=25:


            node.state = "MODERATE"



        else:


            node.state="SAFE"




        node.update_timestamp()








    def get_building_state(self):


        state = {}



        nodes = (

            list(self.building.rooms.items())

            +

            list(self.building.corridors.items())

        )



        for node_id,node in nodes:


            state[node_id]={


                "node_type":
                    node.node_type,


                "temperature":
                    node.temperature,


                "smoke":
                    node.smoke,


                "flame":
                    node.flame,


                "occupancy":
                    node.occupancy,


                "hazard_score":
                    node.hazard_score,


                "predicted_hazard":
                    node.predicted_hazard,


                "prediction":
                    getattr(
                        node,
                        "prediction",
                        {}
                    ),


                "hazard":
                    node.hazard_score,


                "prediction_score":
                    node.predicted_hazard,


                "state":
                    node.state


            }



        return state







    def start(self):


        self.client.on_connect = self.on_connect

        self.client.on_message = self.on_message

        self.client.on_disconnect = self.on_disconnect




        self.client.connect(
            MQTT_BROKER,
            1883,
            keepalive=60
        )

        self.client.loop_forever(retry_first_connection=True)