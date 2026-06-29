import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { User } from '../user.model';
import { UsersService } from '../users.service';
import { AuthService } from '../../auth.service';

@Component({
  selector: 'app-users-management',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './users-management.component.html',
  styleUrls: ['./users-management.component.scss'],
})
export class UsersManagementComponent implements OnInit {
  private readonly usersService = inject(UsersService);
  private readonly authService = inject(AuthService);

  users: User[] = [];
  isLoading = false;
  message = '';
  error = '';

  showForm = false;
  formMode: 'create' | 'edit' = 'create';
  
  selectedUserId: string | null = null;
  deletingUser: User | null = null;
  
  showPassword = false;

  readonly roles = [
    { value: 1, label: 'Nông dân' },
    { value: 2, label: 'Thương lái' },
    { value: 3, label: 'Nhà phân phối' },
    { value: 0, label: 'Admin' },
    { value: 4, label: 'Người tiêu dùng' },
  ];

  form = {
    full_name: '',
    email: '',
    password: '',
    role: 1,
    is_active: true
  };

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.isLoading = true;
    this.usersService.getUsers().subscribe({
      next: (data) => {
        this.users = data;
        this.isLoading = false;
      },
      error: (err) => {
        this.error = 'Lỗi tải danh sách người dùng.';
        this.isLoading = false;
      }
    });
  }

  getRoleLabel(roleValue: number): string {
    const r = this.roles.find(x => x.value === roleValue);
    return r ? r.label : 'Người tiêu dùng';
  }

  openCreateForm(): void {
    this.formMode = 'create';
    this.form = {
      full_name: '',
      email: '',
      password: '',
      role: 1,
      is_active: true
    };
    this.selectedUserId = null;
    this.showForm = true;
    this.message = '';
    this.error = '';
  }

  openEditForm(user: User): void {
    this.formMode = 'edit';
    this.form = {
      full_name: user.full_name,
      email: user.email,
      password: '', // password left blank for edit, not supported yet or ignored
      role: user.role,
      is_active: user.is_active
    };
    this.selectedUserId = user.id;
    this.showForm = true;
    this.message = '';
    this.error = '';
  }

  closeForm(): void {
    this.showForm = false;
  }

  openDeleteConfirm(user: User): void {
    this.deletingUser = user;
    this.message = '';
    this.error = '';
  }

  confirmDelete(): void {
    if (!this.deletingUser) return;
    this.isLoading = true;
    this.usersService.deleteUser(this.deletingUser.id).subscribe({
      next: () => {
        this.message = 'Xóa người dùng thành công.';
        this.deletingUser = null;
        this.loadUsers();
      },
      error: (err) => {
        this.error = err.error?.detail || 'Lỗi khi xóa người dùng.';
        this.isLoading = false;
        this.deletingUser = null;
      }
    });
  }

  submitForm(): void {
    this.message = '';
    this.error = '';
    this.isLoading = true;

    if (this.formMode === 'create') {
      this.authService.register({
        full_name: this.form.full_name.trim(),
        email: this.form.email.trim(),
        password: this.form.password,
        role: this.form.role,
      }).subscribe({
        next: () => {
          this.message = 'Tạo người dùng thành công.';
          this.loadUsers();
          this.closeForm();
        },
        error: (err) => {
          this.error = err.error?.detail || 'Lỗi khi tạo người dùng.';
          this.isLoading = false;
        }
      });
    } else if (this.formMode === 'edit' && this.selectedUserId) {
      this.usersService.updateUser(this.selectedUserId, {
        full_name: this.form.full_name.trim(),
        email: this.form.email.trim(),
        role: this.form.role,
        is_active: this.form.is_active
      }).subscribe({
        next: () => {
          this.message = 'Cập nhật thành công.';
          this.loadUsers();
          this.closeForm();
        },
        error: (err) => {
          this.error = err.error?.detail || 'Lỗi cập nhật người dùng.';
          this.isLoading = false;
        }
      });
    }
  }
}
