from app.domain.rules.risk_strategy import RiskStrategy


class SoilRiskStrategy(RiskStrategy):

    def evaluate(self, sensor_log, rule) -> bool:
        if sensor_log.soil_moisture is None:
            return False
        return (
            sensor_log.soil_moisture < (rule.min_soil_moisture or 0)
            or sensor_log.soil_moisture > (rule.max_soil_moisture or 0)
        )
