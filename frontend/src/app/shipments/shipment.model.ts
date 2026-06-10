export interface ShipmentItem {
  id?: string;
  shipment_id?: string;
  batch_id: string;
  container_id: string;
  quantity: number;
  quantity_unit: string;
}

export interface Shipment {
  id: string;
  from_actor_id: string;
  to_actor_id: string;
  carrier_id: string;
  origin: string;
  destination: string;
  status: number | string;
  start_time: string;
  end_time: string | null;
  notes: string | null;
  items: ShipmentItem[];
}

export interface ShipmentPayload {
  id?: string;
  from_actor_id: string;
  to_actor_id: string;
  carrier_id: string;
  origin: string;
  destination: string;
  status: number | string;
  start_time: string;
  end_time: string | null;
  notes: string | null;
  items: ShipmentItem[];
}
