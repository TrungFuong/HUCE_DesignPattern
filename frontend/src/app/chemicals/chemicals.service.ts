import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Chemical, ChemicalPayload } from './chemical.model';

@Injectable({ providedIn: 'root' })
export class ChemicalsService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = 'http://localhost:8000';

  getChemicals(): Observable<Chemical[]> {
    return this.http.get<Chemical[]>(`${this.apiBaseUrl}/chemicals/`);
  }

  getChemicalsByCropType(cropTypeId: string): Observable<Chemical[]> {
    return this.http.get<Chemical[]>(`${this.apiBaseUrl}/chemicals/crop-type/${cropTypeId}`);
  }

  createChemical(payload: ChemicalPayload): Observable<Chemical> {
    return this.http.post<Chemical>(`${this.apiBaseUrl}/chemicals/`, payload);
  }

  updateChemical(id: string, payload: ChemicalPayload): Observable<Chemical> {
    return this.http.put<Chemical>(`${this.apiBaseUrl}/chemicals/${id}`, payload);
  }

  deleteChemical(id: string): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${this.apiBaseUrl}/chemicals/${id}`);
  }
}
