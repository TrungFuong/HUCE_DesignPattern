from app.domain.rules.risk_strategy import RiskStrategy


class HumidityRiskStrategy(RiskStrategy):

    def evaluate(self, sensor_log, rule) -> bool:
        return (
            sensor_log.humidity < rule.min_humidity
            or sensor_log.humidity > rule.max_humidity
        )
