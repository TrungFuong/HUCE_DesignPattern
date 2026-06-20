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

  updateUser(id: string, payload: Partial<User>): Observable<User> {
    return this.http.put<User>(`${this.apiBaseUrl}/users/${id}`, payload);
  }

  deleteUser(id: string): Observable<any> {
    return this.http.delete(`${this.apiBaseUrl}/users/${id}`);
  }
}
