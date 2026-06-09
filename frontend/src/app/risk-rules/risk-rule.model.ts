export interface RiskRule {
  id: string;
  crop_type_id: string;
  min_temperature: number;
  max_temperature: number;
  min_humidity: number;
  max_humidity: number;
  min_soil_moisture: number | null;
  max_soil_moisture: number | null;
  duration_minutes: number;
}

export interface RiskRulePayload {
  crop_type_id: string;
  min_temperature: number;
  max_temperature: number;
  min_humidity: number;
  max_humidity: number;
  min_soil_moisture: number | null;
  max_soil_moisture: number | null;
  duration_minutes: number;
}

export interface RiskRuleFormValue {
  crop_type_ids: string[];
  min_temperature: number;
  max_temperature: number;
  min_humidity: number;
  max_humidity: number;
  min_soil_moisture: number | null;
  max_soil_moisture: number | null;
  duration_minutes: number;
}
