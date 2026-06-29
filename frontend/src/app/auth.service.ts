import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { BehaviorSubject, Observable, catchError, of, tap } from 'rxjs';
import { User } from './users/user.model';

export type AuthMode = 'login' | 'register';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest extends LoginRequest {
  full_name: string;
  role: number | string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_at: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = 'http://localhost:8000';
  private readonly storageKey = 'ocop_access_token';
  private readonly currentUserSubject = new BehaviorSubject<User | null>(null);

  readonly currentUser$ = this.currentUserSubject.asObservable();

  login(payload: LoginRequest): Observable<AuthResponse> {
    return this.http
      .post<AuthResponse>(`${this.apiBaseUrl}/auth/login`, payload)
      .pipe(tap((response) => this.persistToken(response)));
  }

  register(payload: RegisterRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiBaseUrl}/auth/register`, payload);
  }

  getToken(): string | null {
    return localStorage.getItem(this.storageKey);
  }

  getMe(): Observable<User> {
    const token = this.getToken();
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.get<User>(`${this.apiBaseUrl}/auth/me`, { headers }).pipe(
      tap((user) => this.currentUserSubject.next(user)),
    );
  }

  changePassword(payload: any): Observable<any> {
    const token = this.getToken();
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.put(`${this.apiBaseUrl}/auth/change-password`, payload, { headers });
  }

  logout(): void {
    localStorage.removeItem(this.storageKey);
    this.currentUserSubject.next(null);
  }

  getCurrentUser(): User | null {
    return this.currentUserSubject.value;
  }

  getRole(): number | null {
    return this.currentUserSubject.value?.role ?? null;
  }

  ensureCurrentUser(): Observable<User | null> {
    if (this.currentUserSubject.value) {
      return of(this.currentUserSubject.value);
    }
    if (!this.getToken()) {
      return of(null);
    }
    return this.getMe().pipe(
      catchError(() => {
        this.logout();
        return of(null);
      }),
    );
  }

  private persistToken(response: AuthResponse): void {
    localStorage.setItem(this.storageKey, response.access_token);
  }
}
