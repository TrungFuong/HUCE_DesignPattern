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
    if (!this.token && !this.isTracePage) {
      this.router.navigate(['/']);
    } else if (this.token) {
      this.authService.getMe().subscribe({
        next: (user) => {
          if (this.router.url === '/') {
            void this.router.navigateByUrl(defaultPathForRole(user.role));
          }
        },
        error: () => {
          this.logout();
          this.router.navigate(['/']);
        }
      });
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
  showRegisterPassword = false;

  readonly publicRoleOptions = [
    { value: 1, label: 'Nông dân' },
    { value: 2, label: 'Thương lái' },
    { value: 3, label: 'Nhà phân phối' },
    { value: 4, label: 'Người tiêu dùng' },
  ];

  readonly form = {
    full_name: '',
    email: '',
    password: '',
    role: 1,
  };

  readonly registerForm = {
    full_name: '',
    email: '',
    password: '',
    role: 1,
  };

  setAuthMode(mode: AuthMode): void {
    if (this.authMode === mode) {
      return;
    }

    this.authMode = mode;
    this.authError = '';
    this.authMessage = '';
    this.isSubmitting = false;
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

  submitRegister(): void {
    this.authError = '';
    this.authMessage = '';
    this.isSubmitting = true;

    this.authService.register({
      full_name: this.registerForm.full_name.trim(),
      email: this.registerForm.email.trim(),
      password: this.registerForm.password,
      role: Number(this.registerForm.role),
    }).subscribe({
      next: () => {
        this.isSubmitting = false;
        this.authMessage = 'Đăng ký thành công. Vui lòng đăng nhập để tiếp tục.';
        this.authMode = 'login';
        this.registerForm.full_name = '';
        this.registerForm.email = '';
        this.registerForm.password = '';
        this.registerForm.role = 1;
      },
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
    const normalizedDetail = typeof detail === 'string' ? detail.toLowerCase() : '';

    if (error.status === 401 || normalizedDetail.includes('invalid credential')) {
      this.authError = 'Email hoặc mật khẩu không chính xác.';
      return;
    }

    this.authError =
      typeof detail === 'string'
        ? detail
        : 'Không thể kết nối API xác thực. Hãy kiểm tra backend FastAPI đang chạy ở localhost:8000.';
  }

}
