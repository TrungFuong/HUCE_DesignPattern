export interface Batch {
  id: string;
  farm_id: string;
  crop_type_id: string | null;
  product_name: string;
  harvest_date: string;
  quantity: number;
  quantity_unit: string;
  grade: string | null;
  status: number;
  risk_level: number;
  qr_code_url: string | null;
  chemicals?: BatchChemicalItem[];
}

export interface BatchPayload {
  farm_id: string;
  crop_type_id: string | null;
  product_name: string;
  harvest_date: string;
  quantity: number;
  quantity_unit: string;
  grade: string | null;
}

export interface BatchChemicalItem {
  chemical_id: string;
  applied_at: string | null;
}
