from app.domain.rules.risk_strategy import RiskStrategy


class TemperatureRiskStrategy(RiskStrategy):

    def evaluate(self, sensor_log, rule) -> bool:
        return (
            sensor_log.temperature < rule.min_temperature
            or sensor_log.temperature > rule.max_temperature
        )
