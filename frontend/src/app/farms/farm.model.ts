export interface Farm {
  id: string;
  owner_id: string;
  name: string;
  address: string;
  planting_date: string | null;
  harvest_date: string | null;
}

export interface FarmPayload {
  owner_id: string;
  name: string;
  address: string;
  planting_date: string | null;
  harvest_date: string | null;
}
