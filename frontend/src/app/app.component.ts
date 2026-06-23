import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterOutlet } from '@angular/router';  // ← thêm Router
import { AuthResponse, AuthService } from './auth.service';
import { DashboardComponent } from './dashboard/dashboard.component';

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

  get isTracePage(): boolean {
    return this.router.url.includes('/traceability/') && this.router.url.includes('/public');
  }

  ngOnInit(): void {
    if (!this.token && !this.isTracePage) {
      this.router.navigate(['/']);
    } else if (this.token) {
      this.authService.getMe().subscribe({
        error: () => {
          this.logout();
          this.router.navigate(['/']);
        }
      });
    }
  }

  showLoginPassword = false;

  readonly form = {
    email: '',
    password: '',
  };

  submitAuth(): void {
    this.authError = '';
    this.authMessage = '';
    this.isSubmitting = true;

    const request$ = this.authService.login({
      email: this.form.email.trim(),
      password: this.form.password,
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
    // this.authMessage = 'Đăng nhập thành công. Chào mừng bạn quay lại hệ thống.';
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
