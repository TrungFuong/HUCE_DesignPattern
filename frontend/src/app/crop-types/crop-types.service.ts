import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { CropType, CropTypePayload } from './crop-type.model';

@Injectable({ providedIn: 'root' })
export class CropTypesService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = 'http://localhost:8000';

  getCropTypes(): Observable<CropType[]> {
    return this.http.get<CropType[]>(`${this.apiBaseUrl}/crop-types/`);
  }

  createCropType(payload: CropTypePayload): Observable<CropType> {
    return this.http.post<CropType>(`${this.apiBaseUrl}/crop-types/`, payload);
  }

  updateCropType(id: string, payload: CropTypePayload): Observable<CropType> {
    return this.http.put<CropType>(`${this.apiBaseUrl}/crop-types/${id}`, payload);
  }

  deleteCropType(id: string): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${this.apiBaseUrl}/crop-types/${id}`);
  }
}
