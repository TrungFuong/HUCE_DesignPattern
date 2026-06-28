import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Shipment, ShipmentPayload } from './shipment.model';

@Injectable({ providedIn: 'root' })
export class ShipmentsService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = 'http://localhost:8000';

  getShipments(): Observable<Shipment[]> {
    return this.http.get<Shipment[]>(`${this.apiBaseUrl}/shipments/`);
  }

  getShipment(id: string): Observable<Shipment> {
    return this.http.get<Shipment>(`${this.apiBaseUrl}/shipments/${id}`);
  }

  createShipment(payload: ShipmentPayload): Observable<Shipment> {
    return this.http.post<Shipment>(`${this.apiBaseUrl}/shipments/`, payload);
  }

  updateShipment(id: string, payload: ShipmentPayload): Observable<Shipment> {
    return this.http.put<Shipment>(`${this.apiBaseUrl}/shipments/${id}`, payload);
  }

  deleteShipment(id: string): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${this.apiBaseUrl}/shipments/${id}`);
  }
}
