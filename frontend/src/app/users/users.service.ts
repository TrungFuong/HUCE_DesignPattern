import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { User } from './user.model';

@Injectable({ providedIn: 'root' })
export class UsersService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = 'http://localhost:8000';

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiBaseUrl}/users/`);
  }

  getFarmers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiBaseUrl}/users/?role=1`);
  }
}
