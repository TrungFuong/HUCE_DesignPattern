export interface TraceProduct {
  name: string;
  harvest_date: string;
  quantity: number;
  quantity_unit: string;
  grade: string | null;
  status: string;
  risk_level: string;
}

export interface TraceFarm {
  name: string;
  address: string;
  planting_date: string;
  harvest_date: string;
  owner: { full_name: string; role: string } | null;
}

export interface TraceContainer {
  code: string;
  type: string;
  capacity: number;
  capacity_unit: string;
  material: string;
  is_temperature_controlled: boolean;
  min_temperature: number | null;
  max_temperature: number | null;
  status: string;
  description: string;
}

export interface TraceShipmentItem {
  product_name: string;
  quantity: number;
  quantity_unit: string;
  container: TraceContainer | null;
}

export interface TraceShipment {
  from: { full_name: string; role: string } | null;
  to: { full_name: string; role: string } | null;
  carrier: { full_name: string; role: string } | null;
  origin: string;
  destination: string;
  status: string;
  start_time: string | null;
  end_time: string | null;
  notes: string | null;
  items: TraceShipmentItem[];
}

export interface TraceSensorLog {
  temperature: number | null;
  humidity: number | null;
  soil_moisture: number | null;
  recorded_at: string;
}

export interface TraceVerification {
  is_verified: boolean;
  current_hash: string | null;
  blockchain_hash: string | null;
}

export interface TraceResponse {
  product: TraceProduct;
  farm: TraceFarm | null;
  shipments: TraceShipment[];
  sensor_logs: TraceSensorLog[];
  verification: TraceVerification;
}