export interface CropType {
  id: string;
  code: string;
  name: string;
  description: string | null;
}

export interface CropTypePayload {
  code: string;
  name: string;
  description: string | null;
}
