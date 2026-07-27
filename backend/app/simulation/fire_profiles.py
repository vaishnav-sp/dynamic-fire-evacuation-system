import random


class FireProfile:

    @staticmethod
    def safe():

        return {
            "temperature": random.uniform(24, 30),
            "smoke": random.uniform(0, 10),
            "flame": False,
            "occupancy": random.randint(0, 5)
        }

    @staticmethod
    def warning():

        return {
            "temperature": random.uniform(35, 50),
            "smoke": random.uniform(20, 40),
            "flame": False,
            "occupancy": random.randint(0, 5)
        }

    @staticmethod
    def danger():

        return {
            "temperature": random.uniform(60, 90),
            "smoke": random.uniform(50, 80),
            "flame": True,
            "occupancy": random.randint(0, 5)
        }

    @staticmethod
    def critical():

        return {
            "temperature": random.uniform(90, 140),
            "smoke": random.uniform(80, 100),
            "flame": True,
            "occupancy": random.randint(0, 5)
        }