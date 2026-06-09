import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Farm, FarmPayload } from './farm.model';

@Injectable({ providedIn: 'root' })
export class FarmsService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = 'http://localhost:8000';

  getFarms(): Observable<Farm[]> {
    return this.http.get<Farm[]>(`${this.apiBaseUrl}/farms/`);
  }

  createFarm(payload: FarmPayload): Observable<Farm> {
    return this.http.post<Farm>(`${this.apiBaseUrl}/farms/`, payload);
  }

  updateFarm(id: string, payload: FarmPayload): Observable<Farm> {
    return this.http.put<Farm>(`${this.apiBaseUrl}/farms/${id}`, payload);
  }

  deleteFarm(id: string): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${this.apiBaseUrl}/farms/${id}`);
  }
}
