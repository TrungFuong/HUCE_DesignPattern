import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Container } from './container.model';

@Injectable({ providedIn: 'root' })
export class ContainersService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = 'http://localhost:8000';

  getContainers(): Observable<Container[]> {
    return this.http.get<Container[]>(`${this.apiBaseUrl}/containers/`);
  }
}
