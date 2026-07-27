from app.simulation.scenario_runner import ScenarioRunner


runner = ScenarioRunner()


runner.start(
    node="R2",
    scenario="FLASHOVER",
    duration=30
)