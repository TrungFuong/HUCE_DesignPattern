export interface Container {
  id: string;
  code: string;
  type: string;
  capacity: number;
  capacity_unit: string;
  material: string | null;
  is_temperature_controlled: boolean;
  min_temperature: number | null;
  max_temperature: number | null;
  status: number;
  description: string | null;
}

export interface ContainerPayload {
  id?: string;
  code: string;
  type: string;
  capacity: number;
  capacity_unit: string;
  material: string | null;
  is_temperature_controlled: boolean;
  min_temperature: number | null;
  max_temperature: number | null;
  status: number;
  description: string | null;
}
