import { Component, OnInit, inject } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../auth.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, DatePipe, FormsModule],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {
  private readonly authService = inject(AuthService);

  user: any = null;
  isLoading = true;
  error = '';

  showChangePasswordModal = false;
  isSubmittingPassword = false;
  passwordError = '';
  passwordMessage = '';
  passwordForm = {
    old_password: '',
    new_password: '',
    confirm_password: ''
  };

  showOldPassword = false;
  showNewPassword = false;
  showConfirmPassword = false;

  readonly roles = [
    { value: 1, label: 'Nông dân' },
    { value: 2, label: 'Thương lái' },
    { value: 3, label: 'Nhà phân phối' },
    { value: 0, label: 'Admin' },
  ];

  ngOnInit(): void {
    this.authService.getMe().subscribe({
      next: (data) => {
        this.user = data;
        this.isLoading = false;
      },
      error: (err) => {
        this.error = 'Không thể tải thông tin cá nhân.';
        this.isLoading = false;
      }
    });
  }

  getRoleLabel(roleValue: number): string {
    const r = this.roles.find(x => x.value === roleValue);
    return r ? r.label : 'Unknown';
  }

  openChangePassword(): void {
    this.showChangePasswordModal = true;
    this.passwordError = '';
    this.passwordMessage = '';
    this.passwordForm = { old_password: '', new_password: '', confirm_password: '' };
  }

  closeChangePassword(): void {
    this.showChangePasswordModal = false;
  }

  submitChangePassword(): void {
    this.passwordError = '';
    this.passwordMessage = '';

    if (this.passwordForm.new_password !== this.passwordForm.confirm_password) {
      this.passwordError = 'Mật khẩu xác nhận không khớp.';
      return;
    }

    if (this.passwordForm.new_password.length < 6) {
      this.passwordError = 'Mật khẩu mới phải có ít nhất 6 ký tự.';
      return;
    }

    this.isSubmittingPassword = true;
    this.authService.changePassword({
      old_password: this.passwordForm.old_password,
      new_password: this.passwordForm.new_password
    }).subscribe({
      next: () => {
        this.isSubmittingPassword = false;
        this.passwordMessage = 'Đổi mật khẩu thành công.';
        setTimeout(() => this.closeChangePassword(), 1500);
      },
      error: (err) => {
        this.isSubmittingPassword = false;
        this.passwordError = err.error?.detail || 'Lỗi khi đổi mật khẩu.';
      }
    });
  }
}
