export interface Chemical {
  id: string;
  crop_type_id: string;
  name: string;
  unit: string;
  description: string | null;
}

export interface ChemicalPayload {
  crop_type_id: string;
  name: string;
  unit: string;
  description: string | null;
}
