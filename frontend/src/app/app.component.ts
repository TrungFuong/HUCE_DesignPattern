import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterOutlet } from '@angular/router';
import { AuthMode, AuthResponse, AuthService } from './auth.service';
import { DashboardComponent } from './dashboard/dashboard.component';
import { defaultPathForRole } from './role.guard';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, RouterOutlet, DashboardComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  title = 'OCOP Traceability';
  isSubmitting = false;
  authMessage = '';
  authError = '';
  token = this.authService.getToken();
  authMode: AuthMode = 'login';

  get isTracePage(): boolean {
    return this.router.url.includes('/traceability/') && this.router.url.includes('/public');
  }

  ngOnInit(): void {
    if (!this.token) {
      if (!this.isTracePage) {
        void this.router.navigateByUrl('/');
      }
      return;
    }

    this.authService.ensureCurrentUser().subscribe((user) => {
      if (!user) {
        this.token = null;
        void this.router.navigateByUrl('/');
        return;
      }

      if (this.router.url === '/') {
        void this.router.navigateByUrl(defaultPathForRole(user.role));
      }
    });
  }

  showLoginPassword = false;

  readonly form = {
    full_name: '',
    email: '',
    password: '',
    role: 1,
  };

  setAuthMode(mode: AuthMode): void {
    this.authMode = mode;
    this.authError = '';
    this.authMessage = '';
  }

  submitAuth(): void {
    this.authError = '';
    this.authMessage = '';
    this.isSubmitting = true;

    const request$ = this.authMode === 'login'
      ? this.authService.login({
          email: this.form.email.trim(),
          password: this.form.password,
        })
      : this.authService.register({
          full_name: this.form.full_name.trim(),
          email: this.form.email.trim(),
          password: this.form.password,
          role: this.form.role,
        });

    request$.subscribe({
      next: (response) => this.handleAuthSuccess(response),
      error: (error: HttpErrorResponse) => this.handleAuthError(error),
    });
  }

  logout(): void {
    this.authService.logout();
    this.token = null;
    this.authMessage = 'Đã đăng xuất khỏi phiên làm việc.';
    void this.router.navigateByUrl('/');
  }

  private handleAuthSuccess(response: AuthResponse): void {
    this.token = response.access_token;
    this.authService.getMe().subscribe({
      next: (user) => {
        this.isSubmitting = false;
        void this.router.navigateByUrl(defaultPathForRole(user.role));
      },
      error: () => {
        this.isSubmitting = false;
        this.authService.logout();
        this.token = null;
        this.authError = 'Không thể tải thông tin tài khoản.';
      },
    });
  }

  private handleAuthError(error: HttpErrorResponse): void {
    this.isSubmitting = false;
    const detail = error.error?.detail;
    this.authError =
      typeof detail === 'string'
        ? detail
        : 'Không thể kết nối API xác thực. Hãy kiểm tra backend FastAPI đang chạy ở localhost:8000.';
  }

}
