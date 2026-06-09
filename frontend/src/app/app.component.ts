import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import { AuthMode, AuthResponse, AuthService } from './auth.service';
import { DashboardComponent } from './dashboard/dashboard.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, RouterOutlet, DashboardComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  private readonly authService = inject(AuthService);

  title = 'OCOP Traceability';
  authMode: AuthMode = 'login';
  isSubmitting = false;
  authMessage = '';
  authError = '';
  token = this.authService.getToken();

  readonly roles = [
    { value: 1, label: 'Nông dân' },
    { value: 2, label: 'Thương lái' },
    { value: 3, label: 'Nhà phân phối' },
    { value: 0, label: 'Admin' },
  ];

  readonly form = {
    full_name: '',
    email: '',
    password: '',
    role: 1,
  };

  setMode(mode: AuthMode): void {
    this.authMode = mode;
    this.authError = '';
    this.authMessage = '';
  }

  submitAuth(): void {
    this.authError = '';
    this.authMessage = '';
    this.isSubmitting = true;

    const request$ =
      this.authMode === 'login'
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
  }

  private handleAuthSuccess(response: AuthResponse): void {
    this.isSubmitting = false;
    this.token = response.access_token;
    this.authMessage =
      this.authMode === 'login'
        ? 'Đăng nhập thành công. Chào mừng bạn quay lại hệ thống.'
        : 'Đăng ký thành công. Tài khoản mới đã sẵn sàng sử dụng.';
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
