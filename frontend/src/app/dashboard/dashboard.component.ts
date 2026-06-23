import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent {
  private readonly authService = inject(AuthService);
  @Input() authMessage = '';
  @Output() logoutRequested = new EventEmitter<void>();

  readonly allMenuItems = [
    { path: '/', icon: '⌂', label: 'Tổng quan', exact: true, roles: [0, 1] },
    { path: '/farms', icon: '▦', label: 'Nông trại', exact: false, roles: [0, 1] },
    { path: '/crop-types', icon: '◇', label: 'Loại nông sản', exact: false, roles: [0, 1] },
    { path: '/batches', icon: '◫', label: 'Lô sản phẩm', exact: false, roles: [0, 1, 2] },
    { path: '/risk-rules', icon: '!', label: 'Risk rule', exact: false, roles: [0, 1] },
    { path: '/containers', icon: '▣', label: 'Container', exact: false, roles: [0, 2] },
    { path: '/shipments', icon: '⇄', label: 'Vận chuyển', exact: false, roles: [0, 2, 3] },
    { path: '/users', icon: '👤', label: 'Người dùng', exact: false, roles: [0] },
    { path: '/sensors', icon: '◉', label: 'Cảm biến IoT', exact: false, roles: [0, 1] },
    { path: '/reports', icon: '▤', label: 'Báo cáo', exact: false, roles: [0] },
  ];

  get menuItems() {
    const role = this.authService.getRole();
    return this.allMenuItems.filter((item) => role !== null && item.roles.includes(role));
  }

  logout(): void {
    this.logoutRequested.emit();
  }
}
