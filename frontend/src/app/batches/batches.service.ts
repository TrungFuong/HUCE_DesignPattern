import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Batch, BatchChemicalItem, BatchPayload } from './batch.model';

@Injectable({ providedIn: 'root' })
export class BatchesService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = 'http://localhost:8000';
  private readonly publicBaseUrl = 'http://localhost:4200';

  getBatches(): Observable<Batch[]> {
    return this.http.get<Batch[]>(`${this.apiBaseUrl}/batches/`);
  }

  createBatch(payload: BatchPayload): Observable<Batch> {
    return this.http.post<Batch>(`${this.apiBaseUrl}/batches/`, payload);
  }

  updateBatch(id: string, payload: BatchPayload): Observable<Batch> {
    return this.http.put<Batch>(`${this.apiBaseUrl}/batches/${id}`, payload);
  }

  deleteBatch(id: string): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${this.apiBaseUrl}/batches/${id}`);
  }

  getBatchChemicals(id: string): Observable<BatchChemicalItem[]> {
    return this.http.get<BatchChemicalItem[]>(`${this.apiBaseUrl}/batches/${id}/chemicals`);
  }

  setBatchChemicals(id: string, payload: BatchChemicalItem[]): Observable<BatchChemicalItem[]> {
    return this.http.put<BatchChemicalItem[]>(`${this.apiBaseUrl}/batches/${id}/chemicals`, payload);
  }

  getQrImageUrl(id: string): string {
    return `${this.apiBaseUrl}/batches/${id}/qr-image`;
  }

  getPublicTraceUrl(id: string): string {
    return `${this.publicBaseUrl}/traceability/${id}/public`;
  }
}
