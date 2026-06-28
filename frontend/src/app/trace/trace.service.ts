import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { TraceResponse } from './trace.model';

@Injectable({ providedIn: 'root' })
export class TraceService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = 'http://localhost:8000';

  getPublicTrace(batchId: string): Observable<TraceResponse> {
    return this.http.get<TraceResponse>(`${this.apiBaseUrl}/traceability/${batchId}/public`);
  }
}