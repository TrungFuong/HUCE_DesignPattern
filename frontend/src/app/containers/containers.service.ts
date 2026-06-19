import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Container, ContainerPayload } from './container.model';

@Injectable({ providedIn: 'root' })
export class ContainersService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = 'http://localhost:8000';

  getContainers(): Observable<Container[]> {
    return this.http.get<Container[]>(`${this.apiBaseUrl}/containers/`);
  }

  createContainer(payload: ContainerPayload): Observable<Container> {
    return this.http.post<Container>(`${this.apiBaseUrl}/containers/`, payload);
  }

  updateContainer(id: string, payload: ContainerPayload): Observable<Container> {
    return this.http.put<Container>(`${this.apiBaseUrl}/containers/${id}`, payload);
  }

  deleteContainer(id: string): Observable<{ deleted: boolean }> {
    return this.http.delete<{ deleted: boolean }>(`${this.apiBaseUrl}/containers/${id}`);
  }
}
